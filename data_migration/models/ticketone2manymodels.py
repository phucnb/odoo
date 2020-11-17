from odoo import models, fields, api


class S247Product(models.Model):
    _name = 'helpdesk.ticket_s247_product'

    ticket_id = fields.Many2one('helpdesk.ticket', 'Ticket Id')
    name = fields.Char("Value")
