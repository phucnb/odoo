from odoo import fields, models


class SelectionChild(models.Model):
    _name = 'selection.main'
    _description = 'Module help manager selection B'

    name = fields.Char(string='Name')


class SelectionParent(models.Model):
    _name = 'selection.type'
    _description = 'Module help manager selection A'

    name = fields.Char(string='Name')
    child_ids = fields.One2many('selection.main', 'parent_id', string='Child IDs')


class SelectionChildInherit(models.Model):
    _inherit = 'selection.main'

    parent_id = fields.Many2one('selection.type', string='Parent')
