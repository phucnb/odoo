# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError


class WarrantySearch(models.TransientModel):
    _name = 'warranty.search.wizard'

    ws_serial_number = fields.Many2one('stock.production.lot', string="Product Serial Number")
    ws_warranties = fields.Many2many('warranty.management', 'search_warranties', 'search_id', 'warranty_id', string='Warranties')

    @api.onchange('ws_serial_number')
    def get_warranties(self):
        for i in self:
            if i.ws_serial_number:
                warranties = self.env['warranty.management'].search([('wm_product_serial_no', '=', i.ws_serial_number.id)]).ids
                i.ws_warranties = [[6, 0, warranties]]
