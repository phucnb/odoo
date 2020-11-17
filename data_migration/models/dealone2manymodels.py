from odoo import models, fields, api


class DealersQuoting(models.Model):
    _name = 'crm.lead_dealers_quoting_this_deal'

    partner_id = fields.Many2one('res.partner', 'Partner Id')
    name = fields.Char("Value")


class ProductConsidered(models.Model):
    _name = 'crm.lead_product_s_considered'

    partner_id = fields.Many2one('res.partner', 'Partner Id')
    name = fields.Char("Value")
