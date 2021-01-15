# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class WarrantyType(models.Model):
    _name = 'warranty.type'

    name = fields.Char(string="Warranty Name", required=True)
    wt_units = fields.Selection([('days', 'Day(s)'),
                                 ('months', 'Month(s)'), ('year', 'Year(s)')], string="Unit", default='year')
    wt_period = fields.Integer("Warranty Period", required=True)
    wt_notes = fields.Html(string="Notes")
    wt_is_default = fields.Boolean('Is Default', default=False)

    @api.model
    def create(self, values):
        try:
            res = super(WarrantyType, self).create(values)
            is_defaults = self.env['warranty.type'].search_count([('wt_is_default', '=', True)])
            if is_defaults > 1:
                raise ValidationError('You can\'t  select multiple warranty types as a default.')
            return res
        except Exception as e:
            raise ValidationError(_(str(e)))

    def write(self, values):
        try:
            res = super(WarrantyType, self).write(values)
            is_defaults = self.env['warranty.type'].search_count([('wt_is_default', '=', True)])
            if is_defaults > 1:
                raise ValidationError('You can\'t  select multiple warranty types as a default.')
            return res
        except Exception as e:
            raise ValidationError(_(str(e)))


