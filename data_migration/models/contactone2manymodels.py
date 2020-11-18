from odoo import models, fields, api


class Years(models.Model):
    _name = 'res.partner_years'

    partner_id = fields.Many2one('res.partner', 'Partner Id')
    name = fields.Char("Value")


class BusinessUnit(models.Model):
    _name = 'res.partner_business_unit'

    partner_id = fields.Many2one('res.partner', 'Partner Id')
    name = fields.Char("Value")


class BuyingRole(models.Model):
    _name = 'res.partner_buying_role'

    partner_id = fields.Many2one('res.partner', 'Partner Id')
    name = fields.Char("Value")


class WhatTypeOfSupport(models.Model):
    _name = 'res.partner_what_type_of_support'

    partner_id = fields.Many2one('res.partner', 'Partner Id')
    name = fields.Char("Value")
