# -*- coding: utf-8 -*-
# Copyright 2024-2026 Prabhat
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    packmate_is_kit_parent = fields.Boolean(
        string='Is PackMate Kit Parent',
        compute='_compute_packmate_kit_fields',
        store=True,
        readonly=True,
    )
    packmate_kit_line_id = fields.Many2one(
        'packmate.kit.line',
        string='PackMate Component',
        ondelete='set null',
        copy=False,
        readonly=True,
        index=True,
    )

    @api.depends('product_id', 'product_id.product_tmpl_id.is_packmate_kit')
    def _compute_packmate_kit_fields(self):
        for line in self:
            line.packmate_is_kit_parent = bool(
                line.product_id
                and line.product_id.product_tmpl_id.is_packmate_kit
            )

    def _packmate_expand_kit_line(self):
        """Replace this kit line with its component lines."""
        self.ensure_one()
        if not self.packmate_is_kit_parent:
            return False

        kit = self.product_id.product_tmpl_id
        component_lines = kit.packmate_component_line_ids
        if not component_lines:
            return False

        # Preserve the kit line total by distributing it across component lines.
        kit_line_total = (
            self.price_unit
            * self.product_uom_qty
            * (1 - self.discount / 100.0)
        )
        total_component_value = sum(
            cl.sale_price * cl.quantity for cl in component_lines
        )

        # Prepare component lines
        component_vals = []
        for cl in component_lines:
            component_qty = cl.quantity * self.product_uom_qty
            if not component_qty:
                continue

            component_price = 0.0
            if total_component_value > 0:
                component_line_total = (
                    cl.sale_price * cl.quantity / total_component_value
                ) * kit_line_total
                component_price = component_line_total / component_qty
            elif kit_line_total > 0:
                # Fallback: equal split if no component prices
                component_line_total = kit_line_total / len(component_lines)
                component_price = component_line_total / component_qty

            component_vals.append({
                'order_id': self.order_id.id,
                'product_id': cl.product_id.id,
                'name': f"[{self.product_id.name}] {cl.product_id.name}",
                'product_uom_qty': component_qty,
                'product_uom': cl.product_uom_id.id,
                'price_unit': component_price,
                'discount': 0.0,
                'packmate_kit_line_id': cl.id,
                'sequence': self.sequence + cl.sequence,
                'tax_id': [(6, 0, self.tax_id.ids)],
            })

        # Create component lines first, then remove parent
        self.env['sale.order.line'].create(component_vals)
        self.unlink()
        return True


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    packmate_has_kit_lines = fields.Boolean(
        string='Has PackMate Kits',
        compute='_compute_packmate_has_kit_lines',
    )

    @api.depends('order_line.packmate_is_kit_parent')
    def _compute_packmate_has_kit_lines(self):
        for order in self:
            order.packmate_has_kit_lines = any(
                order.order_line.mapped('packmate_is_kit_parent')
            )

    def action_packmate_expand_all(self):
        """Expand all PackMate kit lines in this order."""
        for order in self:
            # Need to collect first because we're deleting during iteration
            kit_parents = order.order_line.filtered('packmate_is_kit_parent')
            for line in kit_parents:
                line._packmate_expand_kit_line()
        return True

    def action_confirm(self):
        # Auto-expand all kit lines before confirmation
        for order in self:
            kit_parents = order.order_line.filtered('packmate_is_kit_parent')
            for line in kit_parents:
                line._packmate_expand_kit_line()
        return super().action_confirm()
