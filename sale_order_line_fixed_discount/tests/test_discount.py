# -*- coding: utf-8 -*-
import odoo
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError


@odoo.tests.common.tagged('at_install')
class TestSaleOrderLineFixedDiscount(TransactionCase):

    def setUp(self):
        super(TestSaleOrderLineFixedDiscount, self).setUp()
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
        })
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
        })
        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })

    def test_discount_amount_computation(self):
        """Test that discount amount is correctly computed from discount percentage."""
        line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 2.0,
            'price_unit': 100.0,
            'discount': 10.0,  # 10% discount
        })
        # Expected discount amount: (100 * 2) * 10/100 = 200 * 0.1 = 20
        self.assertEqual(line.discount_amount, 20.0)

    def test_discount_percentage_from_amount(self):
        """Test that discount percentage is correctly computed from discount amount."""
        line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 2.0,
            'price_unit': 100.0,
            'discount_amount': 30.0,
        })
        # Expected discount percentage: (30 / (100*2)) * 100 = 15%
        self.assertEqual(line.discount, 15.0)

    def test_discount_amount_validation(self):
        """Test that discount amount cannot exceed line subtotal."""
        with self.assertRaises(ValidationError):
            self.env['sale.order.line'].create({
                'order_id': self.sale_order.id,
                'product_id': self.product.id,
                'product_uom_qty': 1.0,
                'price_unit': 100.0,
                'discount_amount': 150.0,  # exceeds subtotal
            })

    def test_discount_amount_zero(self):
        """Test that discount amount can be zero."""
        line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 1.0,
            'price_unit': 100.0,
            'discount_amount': 0.0,
        })
        self.assertEqual(line.discount, 0.0)
        self.assertEqual(line.discount_amount, 0.0)
