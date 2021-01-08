from odoo import api, fields, models


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    is_log_schedule = fields.Boolean(string='Is Log Schedule')
    callout_come = fields.Selection([
        ('busy', 'Busy'),
        ('noanswer', 'No Answer'),
        ('wrongnumber', 'Wrong Number'),
        ('contactnolongerthere', 'Contact No Longer There'),
        ('didnotconnectwithcontact', 'Did Not Connect With Contact'),
        ('connectedtalkedtocontact', 'Connected (Talked to Contact)'),
        ('connected', 'Connected'),
        ('leftlivemessage', 'Left live message'),
        ('lvmleftvoicemessage', 'LVM (Left Voice Message)')
    ], string='Call Outcome')
    call_type = fields.Selection([
        ('caloutbountcorona', 'Call - Outbound Corona Campaign'),
        ('callinabountcorona', 'Call - Inbound Corona Campaign'),
        ('callclientinbound', 'Call - Client Inbound'),
        ('callclientoutbound', 'Call  - Client Outbound'),
        ('callprospectinbound', 'Call - Prospect Inbound'),
        ('callprospectoutbound', 'Call - Prospect Outbound'),
        ('callfollowup', 'Call - Follow-up'),
        ('callsurvey', 'Call - Survey'),
        ('meetingaccountreview', 'Meeting - Account Review'),
        ('meetingpresentationonline', 'Meeting - Presentation On-line'),
        ('meetingpresentationonsite', 'Meeting - Presentation On-site'),
        ('meetingtrainingonline', 'Meeting  - Training on-line'),
        ('meetingtraningonsite', 'Meeting - Training On-site'),
        ('meetingonsite', 'Meeting - On-site'),
        ('meetingcientprojectkickoff', 'Meeting - Client Project Kick-off'),
        ('meetingtrashowchapter', 'Meeting - Trade Show / Chapter'),
        ('campaignobile', 'Campaign'),
        ('meetingintroductiononsitehone', 'Meeting - Introduction On-site'),
        ('onsiteservice', 'On-Site Service'),
        ('setameetingwithacustomer', 'Set a Meeting/Appointment with a Customer'),
        ('technicalsupport', 'Technical Support'),
        ('technicalissuefollowup', 'Technical Issue Follow-up'),
        ('chaptermeeting', 'Chapter Meeting'),
        ('247contractedfleet', 'S247 Contracted Fleet'),
        ('s247emailedinfo', 'S247 Emailed Info'),
        ('s247quoted', 'S247 Quoted'),
        ('s247scheduledpresentation', 'S247 Scheduled Presentation'),
        ('s247service', 'S247 Service'),
        ('s247notinterested', 'S247 Not Interested'),
        ('campagingpsissue', 'Campaign - GPS issue, 2020')
    ], string='Call and Meeting Type')
    out_come = fields.Selection([
        ('out', 'Out'),
        ('come', 'Come')
    ], string='Out Come')
    is_call_type = fields.Boolean(string='Is Call Type', default=False)
    is_mail_type = fields.Boolean(string='Is Mail Type', default=False)

    @api.model
    def default_get(self, fields):
        res = super(MailActivity, self).default_get(fields)
        if self._context.get('is_log_schedule', False) and not res.get('is_log_schedule', False):
            res['is_log_schedule'] = True
        return res

    @api.onchange('activity_type_id')
    def onchange_activity_id(self):
        if self.activity_type_id:
            call_type_id = self.env.ref('mail.mail_activity_data_call').id
            mail_type_id = self.env.ref('mail.mail_activity_data_email').id
            if self.activity_type_id.id == call_type_id or self.activity_type_id.name == 'Call':
                self.is_call_type = True
                self.is_mail_type = False
            if self.activity_type_id.id == mail_type_id or self.activity_type_id.name == 'Email':
                self.is_mail_type = True
                self.is_call_type = False
        else:
            self.is_mail_type = False
            self.is_call_type = False




