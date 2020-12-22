from odoo import models, fields, api

class TicketFields(models.Model):
    _inherit = 'helpdesk.ticket'

    multiple_product = fields.Boolean("Multiple Product")
    child_ids = fields.One2many(
        'res.partner', 'parent_id',
        string='Contact',
        domain=[('active', '=', True)]
     )  # force "active_test" domain to bypass _search() override
     
     customer_main = fields.Many2one(
            'res.partner', string='Customer'
     )
        
     customer_busaddress = fields.Char(
            string='Bus Garage Address',
            related='customer_main.bus_garage_address', related_sudo=True, compute_sudo=True,
            readonly=True, store=True, index=True
     )