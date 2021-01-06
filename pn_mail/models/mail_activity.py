from odoo import api, fields, models


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    status = fields.Char(string='Status')
    for_txt = fields.Char(string='For')
    is_log_schedule = fields.Boolean(string='Is Log Schedule', default=False)

    @api.onchange('activity_type_id')
    def onchange_activity_type(self):
        is_log_schedule = False
        if self.activity_type_id:
            log_activity_id = self.env.ref('pn_mail.mail_activity_type_log').id
            if self.activity_type_id.id == log_activity_id:
                is_log_schedule = True
        self.is_log_schedule = is_log_schedule
