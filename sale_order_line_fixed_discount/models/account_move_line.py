# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    discount_amount = fields.Float(
        string='Fixed Discount Amount',
        digits='Product Price',
        help="Fixed discount amount applied to the invoice line.",
        compute='_compute_discount_amount',
        inverse='_inverse_discount_amount',
        store=True,
        readonly=False
    )

    @api.depends('price_unit', 'quantity', 'discount')
    def _compute_discount_amount(self):
        """Compute discount amount based on percentage discount."""
        for line in self:
            if line.discount:
                # Standard logic: discount amount = (price_unit * quantity) * (discount / 100)
                base_amount = line.price_unit * line.quantity
                line.discount_amount = base_amount * (line.discount / 100)
            else:
                line.discount_amount = 0.0

    def _inverse_discount_amount(self):
        """Set percentage discount based on discount amount."""
        for line in self:
            if line.discount_amount:
                base_amount = line.price_unit * line.quantity
                if base_amount > 0:
                    line.discount = (line.discount_amount / base_amount) * 100
                else:
                    line.discount = 0.0
            else:
                line.discount = 0.0

    @api.constrains('discount_amount')
    def _check_discount_amount(self):
        """Ensure discount amount does not exceed line subtotal."""
        for line in self:
            if line.discount_amount:
                base_amount = line.price_unit * line.quantity
                if line.discount_amount > base_amount:
                    raise ValidationError(_("Discount amount cannot exceed the line's total price."))
