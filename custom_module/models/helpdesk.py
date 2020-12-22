from odoo import models, fields, api

class TicketFields(models.Model):
    _inherit = 'helpdesk.ticket'

    multiple_product = fields.Boolean("Multiple Product")