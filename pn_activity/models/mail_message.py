from odoo import fields, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    activity_due_date = fields.Date('Due Date', index=True)
