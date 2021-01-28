from odoo import models, fields, api

class dvrType(models.Model):
    _name = 'helpdesk.dvrTypeSelect'

    name = fields.Char("Value")


class camType(models.Model):
    _name = 'helpdesk.camTypeSelect'

    name = fields.Char("Value")

class storageType(models.Model):
    _name = 'helpdesk.storageTypeSelect'

    name = fields.Char("Value")

class apType(models.Model):
    _name = 'helpdesk.apTypeSelect'

    name = fields.Char("Value")

class bridgeType(models.Model):
    _name = 'helpdesk.bridgeTypeSelect'

    name = fields.Char("Value")

class tdType(models.Model):
    _name = 'helpdesk.tdTypeSelect'

    name = fields.Char("Value")

class dvrvType(models.Model):
    _name = 'helpdesk.dvrvTypeSelect'

    name = fields.Char("Value")

class custSysType(models.Model):
    _name = 'helpdesk.custSysType'

    name = fields.Char("Value")
