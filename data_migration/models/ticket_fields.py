from odoo import models, fields, api


SUPPORT_REQUEST = [
    ('< 5min', '< 5min'),
    ('< 15min', '< 15min'),
    ('< 30min', '< 30min'),
    ('> 30min', '> 30min'),
    ('> 1hr', '> 1hr')
]

PRODUCT = [
    ('Touchdown', 'Touchdown'),
    ('ZeusPt', 'ZeusPt'),
    ('Zeus8', 'Zeus8'),
    ('Zeus5', 'Zeus5'),
    ('Zeus3', 'Zeus3'),
    ('30X', '30X'),
    ('514M', '514M'),
    ('51X/600', '51X/600'),
    ('400/500', '400/500'),
    ('S247 DVR Viewer', 'S247 DVR Viewer'),
    ('S247 HDQ Cams', 'S247 HDQ Cams Interior'),
    ('S247 HDQ Cams Exterior', 'S247 HDQ Cams Exterior'),
    ('S247 AHD Cams', 'S247 AHD Cams Interior'),
    ('S247 AHD Cams Exterior', 'S247 AHD Cams Exterior'),
    ('S247 FHD Cams', 'S247 FHD Cams Interior'),
    ('S247 FHD Cams Exterior', 'S247 FHD Cams Exterior'),
    ('S247 OV Cams', 'S247 OV Cams Interior'),
    ('S247 OV Cams Exterior', 'S247 OV Cams Exterior'),
    ('TRS', 'TRS')
]

PW_RESOLUTION = [
    ('PW - Schedule Remote Assistance', 'PW - Schedule Remote Assistance'),
    ('PW - Escalated', 'PW - Escalated'),
    ('PW - Site Visit Scheduled', 'PW - Site Visit Scheduled'),
    ('PW - Site Visit Required', 'PW - Site Visit Required'),
    ('PW - Awaiting Customer Action', 'PW - Awaiting Customer Action'),
    ('PW - Awaiting Partner Action', 'PW - Awaiting Partner Action'),
    ('PW - RMA Required', 'PW - RMA Required'),
    ('PW - Issue Resolved', 'PW - Issue Resolved')
]

S247_PRODUCT = [
    ('1080p Cam', '1080p Cam'),
    ('DHD', 'DHD'),
    ('DHD2', 'DHD2'),
    ('Dual Stop Arm Cam', 'Dual Stop Arm Cam'),
    ('HD Cam', 'HD Cam'),
    ('SD Cam', 'SD Cam'),
    ('Shield Cam', 'Shield Cam'),
    ('Stop Arm Cam', 'Stop Arm Cam'),
    ('Touchdown', 'Touchdown')
]


class TicketFields(models.Model):
    _inherit = 'helpdesk.ticket'

    hubspot_id = fields.Char('Hubspot Id')
    assigned_company = fields.Char("Assigned Company")
    cs_number = fields.Char("CS number")
    support_request = fields.Selection(SUPPORT_REQUEST, "Phone Support Time")
    product = fields.Selection(PRODUCT, 'Product')
    pw_resolution = fields.Selection(PW_RESOLUTION, 'PW Resolution')
    rn_number = fields.Char("RN number")
    s247_resolution = fields.Char('S247 Resolution')
    s247_product = fields.Many2many('get.values', 's247_product_values', 's247_product', 'value', 'S247 Product',
                                    help='Please add/select S247 products e.g. 1080p Cam, DHD, DHD2, Dual Stop Arm Cam,'
                                         ' HD Cam, SD Cam, Shield Cam, Stop Arm Cam and Touchdown') #multiple
    touchdown = fields.Char("Touchdown")
