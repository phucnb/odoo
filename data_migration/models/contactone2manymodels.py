from odoo import models, fields, api


class Years(models.Model):
    _name = 'res.partner_years'

    name = fields.Char("Value")


class BusinessUnit(models.Model):
    _name = 'res.partner_business_unit'

    name = fields.Char("Value")


class BuyingRole(models.Model):
    _name = 'res.partner_buying_role'

    name = fields.Char("Value")


class WhatTypeOfSupport(models.Model):
    _name = 'res.partner_what_type_of_support'

    name = fields.Char("Value")
