from datetime import date, timedelta
from collections import defaultdict

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import ValidationError
from odoo.tools.misc import clean_context


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    state = fields.Selection(
        selection_add=[("done", "Done")],
        compute="_compute_state",
        store=True
    )
    date_done = fields.Date("Completed Date", index=True, readonly=True)
    feedback = fields.Text("Feedback")
    meeting_subject = fields.Char(string='Meeting Subject')
    start_date = fields.Date(string='Starting at')
    end_date = fields.Date(string='Ending at')
    partner_ids = fields.Many2many('res.partner', string='Attendees')
    allday = fields.Boolean('All Day', default=True)
    start = fields.Datetime(
        string='Start', tracking=True, default=fields.Date.today,
        help="Start date of an event, without time for full days events"
    )
    stop = fields.Datetime(
        string='Stop', required=True, tracking=True, default=fields.Date.today,
        compute='_compute_stop', readonly=False, store=True,
        help="Stop date of an event, without time for full days events"
    )
    duration = fields.Float('Duration', compute='_compute_duration', store=True, readonly=False)
    active = fields.Boolean(string='Active', default=True)

    @api.depends('stop', 'start')
    def _compute_duration(self):
        for event in self.with_context(dont_notify=True):
            event.duration = self._get_duration(event.start, event.stop)

    @api.depends('start', 'duration')
    def _compute_stop(self):
        duration_field = self._fields['duration']
        self.env.remove_to_compute(duration_field, self)
        for event in self:
            event.stop = event.start + timedelta(minutes=round((event.duration or 1.0) * 60))
            if event.allday:
                event.stop -= timedelta(seconds=1)

    def _get_duration(self, start, stop):
        if not start or not stop:
            return 0
        duration = (stop - start).total_seconds() / 3600
        return round(duration, 2)

    @api.onchange('allday')
    def onchange_allday_date(self):
        self.start_date = date.today() if self.allday else False
        self.end_date = date.today() if self.allday else False

    @api.onchange('activity_category')
    def onchange_activity_category(self):
        if self.activity_category == 'meeting':
            attendees = self.env.user.partner_id.ids
            if self.res_model and self.res_id:
                active_id = self.env[self.res_model].browse(self.res_id)
                if active_id.exists():
                    if 'partner_id' in active_id and active_id.partner_id:
                        attendees.append(active_id.partner_id.id)
                        customer_company = active_id.partner_id.parent_id
                        company_id = customer_company and customer_company.id or False
                        if company_id:
                            attendees.append(company_id)
                    self.meeting_subject = 'name' in active_id and active_id.name or ''
                if self.res_model == 'res.partner':
                    contact_id = self.env[self.res_model].browse(self.res_id)
                    attendees.append(contact_id.id)
                    if contact_id.parent_id:
                        attendees.append(contact_id.parent_id.id)
            self.partner_ids = [(6, 0, attendees)]
            self.start_date = date.today()
            self.end_date = date.today()
        else:
            self.meeting_subject = ''
            self.start_date = ''
            self.end_date = ''
            self.partner_ids = [(5, 0)]

    def __validate_calendar_event_data(self):
        if not self.meeting_subject:
            raise ValidationError(_("Meeting Subject is not null."))
        if self.allday:
            if not self.start_date or not self.end_date:
                raise ValidationError(_("Meeting Time is not null."))
        if not self.allday:
            if not self.start:
                raise ValidationError(_("Start at is not null"))
            if not self.duration or self.duration < 0:
                raise ValidationError(_("Duration is not null and greater than 0."))

    def action_create_calendar_event_non_setup(self):
        self.__validate_calendar_event_data()
        calendar_event = self.env['calendar.event']
        event_value = {
            'name': self.meeting_subject, 'res_id': self.env.context.get('default_res_id'), 'res_model': self.env.context.get('default_res_model'),
            'description': self.note and tools.html2plaintext(self.note).strip() or '',
            'activity_ids': [(6, 0, self.ids)], 'show_as': 'busy', 'privacy': 'public', 'partner_ids': [(6, 0, self.partner_ids.ids)]
        }
        if self.allday:
            event_value.update({'start_date': self.start_date, 'stop_date': self.end_date, 'allday': True})
        else:
            event_value.update({'start': self.start, 'stop': self.stop, 'allday': False})
        calendar_id = calendar_event.create(event_value)
        return True

    def action_feedback_schedule_next(self, feedback=False):
        ctx = dict(
            clean_context(self.env.context),
            default_previous_activity_type_id=self.activity_type_id.id,
            activity_previous_deadline=self.date_deadline,
            default_res_id=self.res_id,
            default_res_model=self.res_model,
        )
        # will unlink activity, don't access self after that
        messages, next_activities = self._action_done(feedback=feedback)
        if next_activities:
            return False
        return {
            'name': _('Schedule an Activity'),
            'context': ctx,
            'view_mode': 'form',
            'res_model': 'mail.activity',
            'views': [(False, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def _set_action_user_id(self, user_id, mail_activity_id):
        if user_id == SUPERUSER_ID or self.env.user.has_group('base.group_system'):
            user_id = mail_activity_id.user_id and mail_activity_id.user_id.id or SUPERUSER_ID
        return user_id

    def _action_done(self, feedback=False, attachment_ids=None):
        """ Private implementation of marking activity as done: posting a message, deleting activity
            (since done), and eventually create the automatical next activity (depending on config).
            :param feedback: optional feedback from user when marking activity as done
            :param attachment_ids: list of ir.attachment ids to attach to the posted mail.message
            :returns (messages, activities) where
                - messages is a recordset of posted mail.message
                - activities is a recordset of mail.activity of forced automically created activities
        """
        # marking as 'done'
        messages = self.env['mail.message']
        next_activities_values = []

        # Search for all attachments linked to the activities we are about to unlink. This way, we
        # can link them to the message posted and prevent their deletion.
        attachments = self.env['ir.attachment'].search_read([
            ('res_model', '=', self._name),
            ('res_id', 'in', self.ids),
        ], ['id', 'res_id'])

        activity_attachments = defaultdict(list)
        for attachment in attachments:
            activity_id = attachment['res_id']
            activity_attachments[activity_id].append(attachment['id'])

        for activity in self:
            # extract value to generate next activities
            if activity.force_next:
                Activity = self.env['mail.activity'].with_context(
                    activity_previous_deadline=activity.date_deadline)  # context key is required in the onchange to set deadline
                vals = Activity.default_get(Activity.fields_get())

                vals.update({
                    'previous_activity_type_id': activity.activity_type_id.id,
                    'res_id': activity.res_id,
                    'res_model': activity.res_model,
                    'res_model_id': self.env['ir.model']._get(activity.res_model).id,
                })
                virtual_activity = Activity.new(vals)
                virtual_activity._onchange_previous_activity_type_id()
                virtual_activity._onchange_activity_type_id()
                next_activities_values.append(virtual_activity._convert_to_write(virtual_activity._cache))

            # post message on activity, before deleting it
            record = self.env[activity.res_model].browse(activity.res_id)
            user_id = self._set_action_user_id(self._uid, activity)
            company_ids = self.env['res.users'].browse(user_id).company_ids.ids
            record.with_user(user_id).with_context(
                allowed_company_ids=company_ids).message_post_with_view(
                'mail.message_activity_done',
                values={
                    'activity': activity,
                    'feedback': feedback,
                    'display_assignee': activity.user_id != self.env.user
                },
                subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_activities'),
                mail_activity_type_id=activity.activity_type_id.id,
                attachment_ids=[(4, attachment_id) for attachment_id in attachment_ids] if attachment_ids else [],
            )

            # Moving the attachments in the message
            # TODO: Fix void res_id on attachment when you create an activity with an image
            # directly, see route /web_editor/attachment/add
            activity_message = record.message_ids[0]
            message_attachments = self.env['ir.attachment'].browse(activity_attachments[activity.id])
            if message_attachments:
                message_attachments.with_user(user_id).with_context(
                    allowed_company_ids=company_ids
                ).write({
                    'res_id': activity_message.id,
                    'res_model': activity_message._name,
                })
                activity_message.attachment_ids = message_attachments
            activity_message.activity_due_date = activity.date_deadline
            messages |= activity_message
            activity.with_user(user_id).with_context(
                allowed_company_ids=company_ids
            ).write({'state': 'done', 'active': False, 'date_done': date.today(), 'feedback': feedback})
        next_activities = self.env['mail.activity'].create(next_activities_values)
        return messages, next_activities

    @api.model
    def create(self, values):
        res = super(MailActivity, self).create(values)
        self.env['mail.activity.overview'].create({'mail_activity_id': res.id, 'activity_ids': [(6, 0, [res.id])]})
        return res
    
    def unlink(self):
        for record in self:
            overview_id = self.env['mail.activity.overview'].search([('mail_activity_id', '=', record.id)])
            overview_id.unlink()
        return super(MailActivity, self).unlink()


class MailActivityOverview(models.Model):
    _name = 'mail.activity.overview'
    _rec_name = 'res_name'
    _description = 'Module help manager all activity'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    mail_activity_id = fields.Many2one('mail.activity', string='Activity')
    res_name = fields.Char(string='Document Name', related='mail_activity_id.res_name', related_sudo=True, readonly=True, store=True)
    activity_type_id = fields.Many2one('mail.activity.type', related='mail_activity_id.activity_type_id', related_sudo=True, readonly=True, store=True)
    summary = fields.Char('Activity Summary', related='mail_activity_id.summary', related_sudo=True, readonly=True, store=True)
    date_deadline = fields.Date('Due Date', index=True, related='mail_activity_id.date_deadline', related_sudo=True, readonly=True, store=True)
    res_model = fields.Char(string='Document Model', related='mail_activity_id.res_model', readonly=True, store=True, related_sudo=True)
    model_name = fields.Char(string='Document Model', related='mail_activity_id.res_model_id.name', readonly=True, store=True, related_sudo=True)
    activity_ids = fields.Many2many(
        'mail.activity', 'mail_activity_overview_rel', 'overview_id', 'mail_activity_id',
        domain="['|',('active','=',False),('active','=',True)]", context={'active_test': False},
        store=True, compute_sudo=True, string='Summary')
    res_id = fields.Many2oneReference(string='Related Document ID', related='mail_activity_id.res_id', index=True, related_sudo=True, readonly=True, store=True, model_field='res_model')
    state = fields.Selection([
        ('overdue', 'Overdue'),
        ('today', 'Today'),
        ('planned', 'Planned'),
        ("done", "Done")
    ], 'State', related='mail_activity_id.state', readonly=True, store=True, related_sudo=True)
    force_next = fields.Boolean("Trigger Next Activity", related='mail_activity_id.force_next', readonly=True, store=True, related_sudo=True)
    user_id = fields.Many2one('res.users', 'Assigned to', related='mail_activity_id.user_id', index=True, readonly=True, store=True, related_sudo=True)
    request_partner_id = fields.Many2one('res.partner', string='Requesting Partner', related='mail_activity_id.request_partner_id', index=True, readonly=True, store=True, related_sudo=True)
    note = fields.Html('Note', related='mail_activity_id.note', readonly=True, store=True, related_sudo=True, sanitize_style=True)
    partner_user_id = fields.Many2one(
        'res.partner', string='Partner User ID',
        compute='_compute_partner_user_id', compute_sudo=True, index=True, store=True
    )

    # Code sync data via python, Cậu có thể xóa nó và thay bằng SQL.
    @api.model
    def sync_mail_activity_data_to_overview(self):
        mail_activity = self.env['mail.activity'].search([])
        mail_activity_overview_obj = self.env['mail.activity.overview'].sudo()
        for activity_id in mail_activity:
            try:
                mail_activity_overview_obj.create({
                    'mail_activity_id': activity_id.id,
                    'res_name': activity_id.res_name,
                    'activity_type_id': activity_id.activity_type_id.id,
                    'summary': activity_id.summary,
                    'date_deadline': activity_id.date_deadline,
                    'model_name': activity_id.res_model_id.name,
                    'activity_ids': [(6, 0, [activity_id.id])]
                })
            except Exception as e:
                print(e)
                continue

    @api.depends('mail_activity_id', 'res_model', 'res_id')
    def _compute_partner_user_id(self):
        for record in self:
            if record.res_model and record.res_id:
                active_id = self.env[record.res_model].browse(record.res_id)
                if active_id and active_id.exists():
                    if 'partner_id' in active_id and active_id.partner_id:
                        record.partner_user_id = active_id.partner_id.id
                    else:
                        record.partner_user_id = False
                if record.res_model == 'res.partner':
                    contact_id = self.env[record.res_model].browse(record.res_id)
                    record.partner_user_id = contact_id.id
            else:
                record.partner_user_id = 'partner_id' in record.user_id and record.user_id.partner_id and record.user_id.partner_id.id or False

    @staticmethod
    def _set_action_user_id(user_id, mail_activity_id):
        if user_id == SUPERUSER_ID:
            user_id = mail_activity_id.user_id and mail_activity_id.user_id.id or SUPERUSER_ID
        return user_id

    def action_done_multi(self):
        user_id = self._uid
        for record in self:
            user_id = self._set_action_user_id(user_id, record.mail_activity_id)
            record.mail_activity_id.with_user(user_id).with_context(allowed_company_ids=self.env.user.company_ids.ids, mail_activity_quick_update=True).action_done()

    def action_done(self):
        self.ensure_one()
        user_id = self._uid
        user_id = self._set_action_user_id(user_id, self.mail_activity_id)
        return self.mail_activity_id.with_user(user_id).with_context(allowed_company_ids=self.env.user.company_ids.ids, mail_activity_quick_update=True).action_done()

    def action_done_schedule_next(self):
        self.ensure_one()
        user_id = self._uid
        user_id = self._set_action_user_id(user_id, self.mail_activity_id)
        return self.mail_activity_id.with_user(user_id).with_context(allowed_company_ids=self.env.user.company_ids.ids, mail_activity_quick_update=True).action_done_schedule_next()

    def action_done_schedule_next(self):
        self.ensure_one()
        user_id = self._uid
        user_id = self._set_action_user_id(user_id, self.mail_activity_id)
        return self.mail_activity_id.with_user(user_id).with_context(allowed_company_ids=self.env.user.company_ids.ids, mail_activity_quick_update=True).action_done_schedule_next()

    def action_open_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self.res_model,
            'src_model': 'mail.activity.overview',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_id': self.res_id,
            'context': dict(self._context),
        }