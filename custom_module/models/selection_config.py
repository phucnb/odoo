from odoo import fields, models

#Main


class SelectionChild(models.Model):
    _name = 'selection.main'
    _description = 'Module help manager selection B'

    name = fields.Char(string='Name')

class SelectionChildInherit(models.Model):
    _inherit = 'selection.main'

    parent_id = fields.Many2one('selection.type', string='Parent')
    
class SelectionParent(models.Model):
    _name = 'selection.type'
    _description = 'Module help manager selection A'

    name = fields.Char(string='Name')
    child_ids = fields.One2many('selection.main', 'parent_id', string='Child IDs')

# #Issue
# class SelectionIssue(models.Model):
#     _name = 'selection.issue'
#     _description = 'Module help manager selection B'

#     name = fields.Char(string='Name')

# class SelectionIssueInherit(models.Model):
#     _inherit = 'selection.issue'

#     parent_id = fields.Many2one('selection.type', string='Parent')

# class SelectionParent2(models.Model):
#     _name = 'selection.type'
#     _description = 'Module help manager selection A'

#     name = fields.Char(string='Name')
#     child_ids = fields.One2many('selection.issue', 'parent_id', string='Child IDs')

# # Resolution
# class SelectionResolution(models.Model):
#     _name = 'selection.resolution'
#     _description = 'Module help manager selection B'

#     name = fields.Char(string='Name')

# class SelectionResolutionInherit(models.Model):
#     _inherit = 'selection.resolution'

#     parent_id = fields.Many2one('selection.type', string='Parent')

# class SelectionParent3(models.Model):
#     _name = 'selection.type'
#     _description = 'Module help manager selection A'

#     name = fields.Char(string='Name')
#     child_ids = fields.One2many('selection.resolution', 'parent_id', string='Child IDs')
