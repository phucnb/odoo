# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
from dateutil.relativedelta import *
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError


class Warranty(models.Model):
    _name = 'warranty.management'

    wm_sale_order_id = fields.Many2one('sale.order', string="Related Sale order")
    wm_start_date = fields.Date("Start Date")
    wm_end_date = fields.Date("End Date")
    wm_partner_id = fields.Many2one('res.partner', string="Customer")
    wm_product_id = fields.Many2one('product.product', string="Product")
    wm_product_serial_no = fields.Many2one('stock.production.lot', string='Product Serial Number')
    wm_status = fields.Selection([('draft', 'Draft'), ('warranty', 'In warranty'),
                                 ('expired', 'Expired')], string="Status", default='draft')
    wm_assigned_by = fields.Many2one('res.users', string="Awarded by")
    wm_comments = fields.Text("Note")
    kanban_state = fields.Selection([
        ('normal', 'Grey'),
        ('done', 'Green'),
        ('blocked', 'Red')], string='Kanban State',
        default='normal', required=True, compute="_compute_kanban_state")
    wm_extended_date = fields.Datetime("Extended Date")
    wm_type = fields.Many2one("warranty.type", "Warranty Type")

    @api.onchange('wm_end_date', 'wm_extended_date')
    def _check_expire(self):
        for i in self:
            current_date = datetime.now()
            if i.wm_extended_date:
                if current_date.date() > i.wm_extended_date:
                    i.wm_status = 'expired'
            else:
                if i.wm_end_date:
                    if current_date.date() > i.wm_end_date:
                        i.wm_status = 'expired'

    def _compute_kanban_state(self):
        for i in self:
            if i.wm_status == 'draft':
                i.kanban_state = 'normal'
            elif i.wm_status == 'warranty':
                i.kanban_state = 'done'
            else:
                i.kanban_state = 'blocked'

    def activatethewarranty(self):
        for i in self:
            i.wm_status = 'warranty'

    def expirethewarranty(self):
        for i in self:
            i.wm_status = 'expired'


class InheritP(models.Model):
    _inherit = 'product.template'

    warranty_type = fields.Many2one('warranty.type', 'Warranty Type')
    warranty_count = fields.Integer("Warranty Count", compute="_compute_warranty_count")

    def _compute_warranty_count(self):
        for product in self:
            product.warranty_count = self.env['warranty.management'].search_count([('wm_product_id', '=', product.id)])

    def get_warranties(self):
        pass

class InheritSP(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        self.ensure_one()
        if not self.move_lines and not self.move_line_ids:
            raise UserError(_('Please add some items to move.'))

        IrConfigParameter = self.env['ir.config_parameter'].sudo()
        auto_confirm = IrConfigParameter.get_param('warranty_management.wm_is_auto_confirm')
        adding_more = None

        current_date = datetime.now()
        end_date = None
        lines = self.sale_id.order_line
        adding_more = 0
        for line in lines:
            product_warranty_type = line.product_id.warranty_type
            if product_warranty_type:
                warranty_units = product_warranty_type.wt_units
                warranty_period = product_warranty_type.wt_period
                if warranty_units == 'days':
                    end_date = current_date + timedelta(days=int(warranty_period))
                elif warranty_units == 'months':
                    end_date = current_date + relativedelta(months=+1)
                elif warranty_units == 'year':
                    end_date = current_date + relativedelta(years=+1)

                for lot_id in self.move_line_ids_without_package.lot_id.ids:
                    warranty = self.env['warranty.management'].search([('wm_sale_order_id', '=', self.sale_id.id),
                                                                       ('wm_product_serial_no', '=', lot_id)])

                    if not warranty:
                        self.env['warranty.management'].create({
                            'wm_type': product_warranty_type.id,
                            "wm_sale_order_id": self.sale_id.id,
                            'wm_product_serial_no': lot_id,
                            "wm_start_date": current_date.date(),
                            "wm_end_date": end_date.date(),
                            "wm_partner_id": self.partner_id.id,
                            "wm_product_id": line.product_id.id,
                            "wm_status": 'warranty' if auto_confirm == 'True' and end_date else 'draft',
                            "wm_assigned_by": self.env.user.id,
                            "wm_comments": "Activating warranty while fulfilment of the order",
                        })

            self.env.cr.commit()

        # Clean-up the context key at validation to avoid forcing the creation of immediate
        # transfers.
        ctx = dict(self.env.context)
        ctx.pop('default_immediate_transfer', None)
        self = self.with_context(ctx)

        # add user as a follower
        self.message_subscribe([self.env.user.partner_id.id])

        # If no lots when needed, raise error
        picking_type = self.picking_type_id
        precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in
                                 self.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
        no_reserved_quantities = all(
            float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in
            self.move_line_ids)
        if no_reserved_quantities and no_quantities_done:
            raise UserError(_(
                'You cannot validate a transfer if no quantites are reserved nor done. To force the transfer, switch in edit more and encode the done quantities.'))

        if picking_type.use_create_lots or picking_type.use_existing_lots:
            lines_to_check = self.move_line_ids
            if not no_quantities_done:
                lines_to_check = lines_to_check.filtered(
                    lambda line: float_compare(line.qty_done, 0,
                                               precision_rounding=line.product_uom_id.rounding)
                )

            for line in lines_to_check:
                product = line.product_id
                if product and product.tracking != 'none':
                    if not line.lot_name and not line.lot_id:
                        raise UserError(
                            _('You need to supply a Lot/Serial number for product %s.') % product.display_name)

        # Propose to use the sms mechanism the first time a delivery
        # picking is validated. Whatever the user's decision (use it or not),
        # the method button_validate is called again (except if it's cancel),
        # so the checks are made twice in that case, but the flow is not broken
        sms_confirmation = self._check_sms_confirmation_popup()
        if sms_confirmation:
            return sms_confirmation

        if no_quantities_done:
            view = self.env.ref('stock.view_immediate_transfer')
            wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, self.id)]})
            return {
                'name': _('Immediate Transfer?'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'stock.immediate.transfer',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }

        if self._get_overprocessed_stock_moves() and not self._context.get('skip_overprocessed_check'):
            view = self.env.ref('stock.view_overprocessed_transfer')
            wiz = self.env['stock.overprocessed.transfer'].create({'picking_id': self.id})
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'stock.overprocessed.transfer',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }

        # Check backorder should check for other barcodes
        if self._check_backorder():
            return self.action_generate_backorder_wizard()
        self.action_done()

        return


class InheritRPL(models.TransientModel):
    _inherit = 'stock.return.picking.line'

    is_warranty = fields.Boolean(string='Is in Warranty', compute='_get_is_warranty')

    @api.onchange('product_id')
    def _get_is_warranty(self):
        for i in self:
            saleorder = i.wizard_id.picking_id.sale_id.id
            lines = i.wizard_id.picking_id.sale_id.order_line
            for line in lines:
                warranty = self.env['warranty.management'].search([('wm_sale_order_id', '=', saleorder),
                                                                   ('wm_product_id', '=', line.product_id.id),
                                                                   ('wm_status', '=', 'warranty')])
                if warranty:
                    i.is_warranty = True
                else:
                    i.is_warranty = False
