from odoo import api, fields, models


class PNMailMessage(models.Model):
    _inherit = 'mail.message'
    _order = 'date desc'

    # TO DO
