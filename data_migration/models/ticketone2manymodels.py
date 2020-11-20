from odoo import models, fields, api


class S247Product(models.Model):
    _name = 'helpdesk.ticket_s247_product'

    name = fields.Char("Value")
