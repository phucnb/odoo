from odoo import api, fields, models, _


class ContactControlActivityMess(models.Model):
    _inherit = 'res.partner'

    activity_count = fields.Integer(string='Activity Count', compute='_compute_activity_count', default=0)
    mail_message_count = fields.Integer(string='Mail Count', compute='_compute_mail_message_count', default=0)

    def _compute_activity_count(self):
        activity_model = self.env['mail.activity.overview']
        for record in self:
            activity_ids = activity_model.search([
                '|', ('partner_user_id', '=', record.id), ('partner_user_id.parent_id', 'child_of', [record.id])
            ])
            record.activity_count = activity_ids and len(activity_ids.ids) or 0

    def _compute_mail_message_count(self):
        for record in self:
            record.mail_message_count = 0

    def action_view_all_activity_control(self):
        self.ensure_one()
        return {
            'name': _('Activity Management'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'mail.activity.overview',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': ['|', ('partner_user_id', '=', self.id), ('partner_user_id.parent_id', 'child_of', [self.id])],
            'context': dict(self._context, search_default_fl_activity=True),
        }

    def action_view_all_mail_message_control(self):
        self.ensure_one()
        try:
            tree_view_id = self.env.ref('pn_customer.pn_customer_mail_message_tree_view', False).id
            form_view_id = self.env.ref('pn_customer.pn_customer_mail_message_form_view', False).id
            return {
                'name': _('Mail/Message'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'mail.message',
                'type': 'ir.actions.act_window',
                'domain': [('message_type', 'in', ['email', 'comment']),
                    '|', ('mail_partner_id', '=', self.id), ('mail_partner_id.parent_id', 'child_of', [self.id])
                ],
                'context': dict(self._context, search_default_fl_activity=True),
                'target': 'current'
            }
        except Exception as e:
            return
