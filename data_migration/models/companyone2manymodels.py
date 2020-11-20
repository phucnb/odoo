from odoo import models, fields, api


class DealerSoldThrough(models.Model):
    _name = 'res.partner_dealer_sold_through'

    partner_id = fields.Many2one('res.partner', 'Partner Id')
    name = fields.Char("Value")


class System(models.Model):
    _name = 'res.partner_system'

    partner_id = fields.Many2one('res.partner', 'Partner Id')
    name = fields.Char("Value")


class CameraSystem(models.Model):
    _name = 'res.partner_camera_system'

    partner_id = fields.Many2one('res.partner', 'Partner Id')
    name = fields.Char("Value")


class HowManyLots(models.Model):
    _name = 'res.partner_how_many_lots_'

    partner_id = fields.Many2one('res.partner', 'Partner Id')
    name = fields.Char("Value")


class Competitor(models.Model):
    _name = 'res.partner_competitor'

    partner_id = fields.Many2one('res.partner', 'Partner Id')
    name = fields.Char("Value")


class PreviousCameraSystem(models.Model):
    _name = 'res.partner_previous_camera_system'

    partner_id = fields.Many2one('res.partner', 'Partner Id')
    name = fields.Char("Value")


class WebTechnologies(models.Model):
    _name = 'res.partner_web_technologies'

    partner_id = fields.Many2one('res.partner', 'Partner Id')
    name = fields.Char("Value")


class TerritoriesCoverage(models.Model):
    _name = 'res.partner_territory_coverage'

    partner_id = fields.Many2one('res.partner', 'Partner Id')
    name = fields.Char("Value")