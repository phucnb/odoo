from odoo import models, fields, api

class TicketFields(models.Model):
    _inherit = 'helpdesk.ticket'

    multiple_product = fields.Boolean("Multiple Product")
    partner_bus_garage_address = fields.Char(string='Bus Garage Address', compute='_compute_partner_info', store=True, readonly=False)


    def _compute_partner_info(self):
        for ticket in self:
            if ticket.partner_id:
                ticket.partner_bus_garage_address = ticket.partner_id.bus_garage_address
                