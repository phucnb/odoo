from odoo import models, fields, api


class CustomActivity(models.Model):
    _inherit = 'mail.message'

    engagement_id = fields.Char()


class CustomActivity(models.Model):
    _inherit = 'mail.activity'

    engagement_id = fields.Char()
    hubspot_status = fields.Char('Status')
    # for call
    forObjectType = fields.Char('For')
    toNumber = fields.Char('To Number')
    fromNumber = fields.Char('From Number')
    durationMilliseconds = fields.Char('Call Duration')
    recordingUrl = fields.Char('Recording URL')
    disposition = fields.Char('Disposition')
    # for meetings
    startTime = fields.Datetime('Start Time')
    endTime = fields.Datetime('End Time')