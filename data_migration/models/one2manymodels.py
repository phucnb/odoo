from odoo import models, fields, api


class DealerSoldThrough(models.Model):
    _name = 'res.partner_dealer_sold_through'

    partner_id = fields.Many2one('res.partner', 'Partner Id')
    name = fields.Char("Value")