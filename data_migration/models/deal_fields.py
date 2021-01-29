from odoo import models, fields, api

S247_LIFECYCLE_STAGE = [
    ('Active Client', 'Active Client'),
    ('Past Client', 'Past Client'),
    ('Prospect', 'Prospect')
]

ISR = [
    ('Ross Evert', 'Ross Evert'),
    ('Brian Sapp', 'Brian Sapp'),
    ('Kristi Keaton', 'Kristi Keaton'),
    ('Client Relations', 'Client Relations'),
    ('FrankGazeley', 'FrankGazeley')
]

PRODUCTS_CONSIDERED = [
    ('ZeusPT', 'ZeusPT'),
    ('ZeusHD', 'ZeusHD'),
    ('Touchdown™', 'Touchdown™'),
    ('GPS', 'GPS'),
    ('G-Force', 'G-Force'),
    ('IP Cameras w/SARAH4\'s', 'IP Cameras w/SARAH4\'s'),
    ('Stop Arm Cameras', 'Stop Arm Cameras'),
    ('Demo', 'Demo'),
    ('Install', 'Install'),
    ('TRS', 'TRS')

]


class DealFields(models.Model):
    _inherit = 'crm.lead'

    hubspot_id = fields.Char('Hubspot Id')
    hs_deal_contacts = fields.Many2many('res.partner', 'deal_contact_rel', 'partner_id', 'deal_id', 'Contacts')
    hs_deal_companies = fields.Many2one('res.partner', 'Company')
    n247s_lifecycle_stage = fields.Selection(S247_LIFECYCLE_STAGE, "247S Lifecycle Stage")
    dealers_quoting_this_deal = fields.Many2many('crm.lead_dealers_quoting_this_deal',
                                                 'opportunity_id_dealers_quoting_this_deal', 'opportunity_id',
                                                 'dealers_quoting_this_deal', 'Dealers quoting this deal',
                                                 help='Please add/select the dealers quoting e.g. A-Z Bus Sales, '
                                                      'Bryson, KLC, Midwest Transit, Rush')
    end_user = fields.Char("End-User")
    isr = fields.Selection(ISR, "ISR")
    lost_reason_notes = fields.Text("Lost Reason Notes")
    opportunity_number = fields.Char("Opportunity Number")
    opportunity_link = fields.Char("Opportunity Link")
    product_s_considered = fields.Many2many('crm.lead_product_s_considered', 'opportunity_id_product_s_considered',
                                            'opportunity_id', 'product_s_considered', 'Products Considered',
                                            help='Please add/select the considered products e.g. ZeusPT, ZeusHD, '
                                                 'Touchdown™, GPS, G-Force, IP Cameras w/SARAH4\'s, Stop Arm Cameras,'
                                                 'Demo, Install, TRS')
    quote_link = fields.Char("Quote Link")
    quote_number = fields.Char("Quote Number")
    sales_number = fields.Char("Sales Number")
    state = fields.Char('State/Region')
    deal_owner = fields.Many2one(
        'res.users', string='Deal Owner'
    )