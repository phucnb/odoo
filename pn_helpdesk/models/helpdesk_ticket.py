from odoo import api, fields, models


class HelpdeskTicketLines(models.Model):
    _name = 'helpdesk.ticket.line'
    _description = 'Helpdesk ticket Line'

    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket')
    type_id = fields.Many2one('helpdesk.ticket.type', string='Type', required=True)
    product_id = fields.Many2one('helpdesk.ticket.product', string='Product')
    issue_id = fields.Many2one('helpdesk.ticket.issue', string='Issue')
    resolution_id = fields.Many2one('helpdesk.ticket.resolution', string='Resolution')
    remark = fields.Text(string='Remark')
    is_change = fields.Boolean(
        string='Is Change', default=False,
        compute='_compute_ticket_line', compute_sudo=True
    )

    @api.onchange('ticket_id')
    def onchange_ticket_id(self):
        if self.ticket_id:
            self.resolution_id = False
            self.product_id = False
            self.issue_id = False


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    line_ids = fields.One2many('helpdesk.ticket.line', 'ticket_id', string='Lines')
