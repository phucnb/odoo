# -*- coding: utf-8 -*-
from odoo import models, fields, api


class InheritRP(models.Model):
    _inherit = 'res.partner'

    netsuite_id = fields.Char("NetSuite Id")
    custentityare_they_buying_new_busses = fields.Boolean("Are they buying new busses?")
    custentity34 = fields.Boolean("34")
    custentity43 = fields.Boolean("43")
    custentity46 = fields.Boolean("46")

