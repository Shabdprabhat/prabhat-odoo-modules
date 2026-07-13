# -*- coding: utf-8 -*-
# Copyright 2024-2026 Prabhat
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PackmateKitLine(models.Model):
    _name = 'packmate.kit.line'
    _description = 'PackMate Kit Component'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    kit_template_id = fields.Many2one(
        'product.template',
        string='Kit Product',
        required=True,
        ondelete='cascade',
        index=True,
        check_company=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        index=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    product_id = fields.Many2one(
        'product.product',
        string='Component',
        required=True,
        domain="[('sale_ok', '=', True), ('id', '!=', parent.product_variant_id)]",
        check_company=True,
    )
    product_uom_id = fields.Many2one(
        'uom.uom',
        string='Unit of Measure',
        related='product_id.uom_id',
        store=True,
        readonly=True,
    )
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    sale_price = fields.Float(
        string='Component Sales Price',
        related='product_id.lst_price',
        readonly=True,
        digits='Product Price',
    )
    cost_price = fields.Float(
        string='Component Cost',
        related='product_id.standard_price',
        readonly=True,
        digits='Product Price',
        groups='base.group_user',
    )
    subtotal_sale_price = fields.Monetary(
        string='Sales Subtotal',
        compute='_compute_subtotals',
        currency_field='currency_id',
    )
    subtotal_cost_price = fields.Monetary(
        string='Cost Subtotal',
        compute='_compute_subtotals',
        currency_field='currency_id',
        groups='base.group_user',
    )

    @api.depends('quantity', 'sale_price', 'cost_price')
    def _compute_subtotals(self):
        for line in self:
            line.subtotal_sale_price = line.quantity * line.sale_price
            line.subtotal_cost_price = line.quantity * line.cost_price

    @api.constrains('quantity')
    def _check_quantity(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError(_('PackMate component quantity must be greater than zero.'))

    @api.constrains('kit_template_id', 'product_id')
    def _check_not_self_component(self):
        for line in self:
            if line.product_id.product_tmpl_id == line.kit_template_id:
                raise ValidationError(_('A PackMate kit cannot contain itself as a component.'))


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_packmate_kit = fields.Boolean(
        string='PackMate Kit',
        help='Enable this product as a sellable kit, combo pack, or product bundle.',
        tracking=True,
    )
    packmate_component_line_ids = fields.One2many(
        'packmate.kit.line',
        'kit_template_id',
        string='PackMate Components',
        copy=True,
    )
    packmate_price_mode = fields.Selection(
        [
            ('manual', 'Manual Price'),
            ('components', 'From Components'),
        ],
        string='Kit Sales Price',
        default='components',
        required=True,
    )
    packmate_cost_mode = fields.Selection(
        [
            ('manual', 'Manual Cost'),
            ('components', 'From Components'),
        ],
        string='Kit Cost',
        default='components',
        required=True,
    )
    packmate_component_count = fields.Integer(
        string='Components',
        compute='_compute_packmate_component_count',
    )
    packmate_component_sales_total = fields.Monetary(
        string='Component Sales Total',
        compute='_compute_packmate_totals',
        currency_field='currency_id',
    )
    packmate_component_cost_total = fields.Monetary(
        string='Component Cost Total',
        compute='_compute_packmate_totals',
        currency_field='currency_id',
        groups='base.group_user',
    )

    @api.depends('packmate_component_line_ids')
    def _compute_packmate_component_count(self):
        for template in self:
            template.packmate_component_count = len(template.packmate_component_line_ids)

    @api.depends(
        'packmate_component_line_ids.quantity',
        'packmate_component_line_ids.sale_price',
        'packmate_component_line_ids.cost_price',
    )
    def _compute_packmate_totals(self):
        for template in self:
            template.packmate_component_sales_total = sum(
                template.packmate_component_line_ids.mapped('subtotal_sale_price')
            )
            template.packmate_component_cost_total = sum(
                template.packmate_component_line_ids.mapped('subtotal_cost_price')
            )

    @api.onchange('is_packmate_kit')
    def _onchange_is_packmate_kit(self):
        if self.is_packmate_kit:
            self.type = 'service'

    def write(self, vals):
        is_kit = vals.get('is_packmate_kit')
        if is_kit:
            vals.setdefault('type', 'service')
        res = super().write(vals)
        if any(field in vals for field in ('packmate_price_mode', 'packmate_cost_mode', 'packmate_component_line_ids')):
            self.filtered('is_packmate_kit')._packmate_apply_component_amounts()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_packmate_kit'):
                vals.setdefault('type', 'service')
        records = super().create(vals_list)
        records.filtered('is_packmate_kit')._packmate_apply_component_amounts()
        return records

    def action_packmate_recompute_amounts(self):
        self._packmate_apply_component_amounts()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'message': _('Kit prices recomputed from components.'),
                'sticky': False,
            },
        }

    def _packmate_apply_component_amounts(self):
        for template in self.filtered('is_packmate_kit'):
            values = {}
            if template.packmate_price_mode == 'components':
                values['list_price'] = template.packmate_component_sales_total
            if template.packmate_cost_mode == 'components':
                values['standard_price'] = template.packmate_component_cost_total
            if values:
                super(ProductTemplate, template).write(values)

    @api.constrains('is_packmate_kit', 'packmate_component_line_ids')
    def _check_packmate_components(self):
        for template in self:
            if template.is_packmate_kit and not template.packmate_component_line_ids:
                raise ValidationError(_('Add at least one component before saving a PackMate kit.'))
