from odoo import api, fields, models


class HelpTicketType(models.Model):
    _name = 'helpdesk.ticket.type'
    _description = 'Helpdesk ticket'

    name = fields.Char(string='Name')


class HelpdeskTicketProduct(models.Model):
    _name = 'helpdesk.ticket.product'
    _description = 'Helpdesk ticket product'

    name = fields.Char(string='Name')
    ticket_type_id = fields.Many2one('helpdesk.ticket.type', string='Ticket Type')


class HelpdeskTicketIssue(models.Model):
    _name = 'helpdesk.ticket.issue'
    _description = 'Helpdesk ticket issue'

    name = fields.Char(string='Name')
    ticket_type_id = fields.Many2one('helpdesk.ticket.type', string='Ticket Type')


class HelpdeskTicketResolution(models.Model):
    _name = 'helpdesk.ticket.resolution'
    _description = 'Helpdesk resolution product'

    name = fields.Char(string='Name')
    ticket_type_id = fields.Many2one('helpdesk.ticket.type', string='Ticket Type')
