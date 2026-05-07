# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import json


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def open_barcode_scanner(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Scan Barcode',
            'res_model': 'barcode.scanner.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id': self.id,
                'default_model': 'sale.order',
            }
        }


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def open_barcode_scanner(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Scan Barcode',
            'res_model': 'barcode.scanner.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id': self.id,
                'default_model': 'purchase.order',
            }
        }


class BarcodeScannerWizard(models.TransientModel):
    _name = 'barcode.scanner.wizard'
    _description = 'Barcode Scanner Wizard'

    barcode = fields.Char(string='Barcode / Product Name')
    order_id = fields.Integer(string='Order ID')
    model = fields.Char(string='Model')

    def action_scan_barcode(self):
        self.ensure_one()
        
        if not self.barcode:
            raise UserError('Please enter a barcode or product name.')
        
        product = self.env['product.product'].search([
            '|', 
            ('barcode', '=', self.barcode),
            ('name', 'ilike', self.barcode)
        ], limit=1)
        
        if not product:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Not Found',
                    'message': 'Product not found for: ' + self.barcode,
                    'type': 'warning'
                }
            }
        
        order_model = self.model
        order_id = self.order_id
        order = self.env[order_model].browse(order_id)
        
        if order_model == 'sale.order':
            order.write({
                'order_line': [(0, 0, {
                    'product_id': product.id,
                    'product_uom_qty': 1,
                    'price_unit': product.list_price,
                })]
            })
        elif order_model == 'purchase.order':
            order.write({
                'order_line': [(0, 0, {
                    'product_id': product.id,
                    'product_qty': 1,
                    'price_unit': product.standard_price,
                })]
            })
        
        self.env['barcode.scan'].create({
            'product_id': product.id,
            'barcode': self.barcode,
            'order_id': str(order.name),
            'order_model': order_model,
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'Added: {product.name}',
                'type': 'success'
            }
        }