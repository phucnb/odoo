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
        # Clean-up the context key at validation to avoid forcing the creation of immediate
        # transfers.
        ctx = dict(self.env.context)
        ctx.pop('default_immediate_transfer', None)
        self = self.with_context(ctx)

        # Sanity checks.
        pickings_without_moves = self.browse()
        pickings_without_quantities = self.browse()
        pickings_without_lots = self.browse()
        products_without_lots = self.env['product.product']
        for picking in self:
            if not picking.move_lines and not picking.move_line_ids:
                pickings_without_moves |= picking

            picking.message_subscribe([self.env.user.partner_id.id])
            picking_type = picking.picking_type_id
            precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in picking.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
            no_reserved_quantities = all(float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in picking.move_line_ids)
            if no_reserved_quantities and no_quantities_done:
                pickings_without_quantities |= picking

            if picking_type.use_create_lots or picking_type.use_existing_lots:
                lines_to_check = picking.move_line_ids
                if not no_quantities_done:
                    lines_to_check = lines_to_check.filtered(lambda line: float_compare(line.qty_done, 0, precision_rounding=line.product_uom_id.rounding))
                for line in lines_to_check:
                    product = line.product_id
                    if product and product.tracking != 'none':
                        if not line.lot_name and not line.lot_id:
                            pickings_without_lots |= picking
                            products_without_lots |= product

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

        if not self._should_show_transfers():
            if pickings_without_moves:
                raise UserError(_('Please add some items to move.'))
            if pickings_without_quantities:
                raise UserError(self._get_without_quantities_error_message())
            if pickings_without_lots:
                raise UserError(_('You need to supply a Lot/Serial number for products %s.') % ', '.join(products_without_lots.mapped('display_name')))
        else:
            message = ""
            if pickings_without_moves:
                message += _('Transfers %s: Please add some items to move.') % ', '.join(pickings_without_moves.mapped('name'))
            if pickings_without_quantities:
                message += _('\n\nTransfers %s: You cannot validate these transfers if no quantities are reserved nor done. To force these transfers, switch in edit more and encode the done quantities.') % ', '.join(pickings_without_quantities.mapped('name'))
            if pickings_without_lots:
                message += _('\n\nTransfers %s: You need to supply a Lot/Serial number for products %s.') % (', '.join(pickings_without_lots.mapped('name')), ', '.join(products_without_lots.mapped('display_name')))
            if message:
                raise UserError(message.lstrip())

        # Run the pre-validation wizards. Processing a pre-validation wizard should work on the
        # moves and/or the context and never call `_action_done`.
        if not self.env.context.get('button_validate_picking_ids'):
            self = self.with_context(button_validate_picking_ids=self.ids)
        res = self._pre_action_done_hook()
        if res is not True:
            return res

        # Call `_action_done`.
        if self.env.context.get('picking_ids_not_to_backorder'):
            pickings_not_to_backorder = self.browse(self.env.context['picking_ids_not_to_backorder'])
            pickings_to_backorder = self - pickings_not_to_backorder
        else:
            pickings_not_to_backorder = self.env['stock.picking']
            pickings_to_backorder = self
        pickings_not_to_backorder.with_context(cancel_backorder=True)._action_done()
        pickings_to_backorder.with_context(cancel_backorder=False)._action_done()
        return True


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
