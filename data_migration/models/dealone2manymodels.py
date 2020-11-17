from odoo import models, fields, api


class DealersQuoting(models.Model):
    _name = 'crm.lead_dealers_quoting_this_deal'

    opportunity_id = fields.Many2one('crm.lead', 'Opportunity Id')
    name = fields.Char("Value")


class ProductConsidered(models.Model):
    _name = 'crm.lead_product_s_considered'

    opportunity_id = fields.Many2one('crm.lead', 'Opportunity Id')
    name = fields.Char("Value")
