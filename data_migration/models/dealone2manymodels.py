from odoo import models, fields, api


class DealersQuoting(models.Model):
    _name = 'crm.lead_dealers_quoting_this_deal'

    name = fields.Char("Value")


class ProductConsidered(models.Model):
    _name = 'crm.lead_product_s_considered'

    name = fields.Char("Value")
