# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_planned_table = fields.Integer(
        'Planned Activities Table Limit', default=1)
    sh_all_table = fields.Integer('All Activities Table Limit', default=1)
    sh_completed_table = fields.Integer(
        'Completed Activities Table Limit', default=1)
    sh_due_table = fields.Integer('Due Activities Table Limit', default=1)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_planned_table = fields.Integer(
        'Planned Activities Table Limit', default=1, related='company_id.sh_planned_table',readonly=False)
    sh_all_table = fields.Integer(
        'All Activities Table Limit', default=1, related='company_id.sh_all_table',readonly=False)
    sh_completed_table = fields.Integer(
        'Completed Activities Table Limit', default=1, related='company_id.sh_completed_table',readonly=False)
    sh_due_table = fields.Integer(
        'Due Activities Table Limit', default=1, related='company_id.sh_due_table',readonly=False)
