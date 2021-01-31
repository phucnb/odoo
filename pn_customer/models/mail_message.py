from odoo import api, fields, models


class MailMessageInherit(models.Model):
    _inherit = 'mail.message'

    mail_partner_id = fields.Many2one(
        'res.partner', string='Partner User ID',
        compute='_compute_partner_user_id', compute_sudo=True, store=True,
        ondelete="set null"
    )

    @api.depends('model', 'res_id')
    def _compute_partner_user_id(self):
        for record in self:
            if record.model and record.res_id:
                active_id = self.env[record.model].browse(record.res_id)
                if active_id and active_id.exists():
                    if 'partner_id' in active_id and active_id.partner_id:
                        record.mail_partner_id = active_id.partner_id.id
                        continue
                    record.mail_partner_id = False
                if record.model == 'res.partner':
                    contact_id = self.env[record.model].browse(record.res_id)
                    if contact_id and contact_id.exists():
                        record.mail_partner_id = contact_id.id
                    else:
                        record.mail_partner_id = False
                continue
            record.mail_partner_id = False
