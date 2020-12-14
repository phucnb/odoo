from odoo import models, fields, api


class S247Product(models.Model):
    _name = 'helpdesk.ticket_s247_product'

    name = fields.Char("Value")


class Category(models.Model):
    _name = 'helpdesk.hs_ticket_category'

    name = fields.Char("Value")

