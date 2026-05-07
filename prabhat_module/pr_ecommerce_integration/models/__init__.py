# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class EcommerceConfig(models.Model):
    _name = 'ecommerce.config'
    _description = 'E-commerce Configuration'
    _rec_name = 'platform'

    PLATFORM_SELECTION = [
        ('shopify', 'Shopify'),
        ('woocommerce', 'WooCommerce'),
        ('amazon', 'Amazon'),
    ]

    platform = fields.Selection(PLATFORM_SELECTION, string='Platform', required=True)
    name = fields.Char(string='Configuration Name')
    active = fields.Boolean(string='Active', default=True)
    
    api_url = fields.Char(string='API URL')
    api_key = fields.Char(string='API Key / Consumer Key')
    api_secret = fields.Char(string='API Secret / Consumer Secret')
    access_token = fields.Char(string='Access Token')
    
    auto_sync_products = fields.Boolean(string='Auto Sync Products', default=True)
    auto_sync_orders = fields.Boolean(string='Auto Sync Orders', default=True)
    auto_sync_inventory = fields.Boolean(string='Auto Sync Inventory', default=False)
    
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    pricelist_id = fields.fields.Many2one('product.pricelist', string='Pricelist')
    journal_id = fields.Many2one('account.journal', string='Sales Journal')
    
    last_sync_date = fields.Datetime(string='Last Sync Date')
    sync_frequency = fields.Selection([
        ('manual', 'Manual'),
        ('hourly', 'Every Hour'),
        ('daily', 'Daily'),
    ], string='Sync Frequency', default='manual')

    def test_connection(self):
        self.ensure_one()
        if self.platform == 'shopify':
            return {'type': 'ir.actions.client', 'tag': 'display_notification',
                    'params': {'title': 'Info', 'message': 'Shopify connection test - Implement API check',
                               'type': 'info'}}
        elif self.platform == 'woocommerce':
            return {'type': 'ir.actions.client', 'tag': 'display_notification',
                    'params': {'title': 'Info', 'message': 'WooCommerce connection test - Implement API check',
                               'type': 'info'}}
        elif self.platform == 'amazon':
            return {'type': 'ir.actions.client', 'tag': 'display_notification',
                    'params': {'title': 'Info', 'message': 'Amazon connection test - Implement API check',
                               'type': 'info'}}

    def action_sync_products(self):
        self.ensure_one()
        return {'type': 'ir.actions.client', 'tag': 'display_notification',
                'params': {'title': 'Success', 'message': f'Syncing products from {self.platform}...',
                           'type': 'info'}}

    def action_sync_orders(self):
        self.ensure_one()
        return {'type': 'ir.actions.client', 'tag': 'display_notification',
                'params': {'title': 'Success', 'message': f'Syncing orders from {self.platform}...',
                           'type': 'info'}}

    def action_sync_inventory(self):
        self.ensure_one()
        return {'type': 'ir.actions.client', 'tag': 'display_notification',
                'params': {'title': 'Success', 'message': f'Syncing inventory from {self.platform}...',
                           'type': 'info'}}


class EcommerceOrderMapping(models.Model):
    _name = 'ecommerce.order.mapping'
    _description = 'E-commerce Order Mapping'

    platform = fields.Selection([
        ('shopify', 'Shopify'),
        ('woocommerce', 'WooCommerce'),
        ('amazon', 'Amazon'),
    ], string='Platform')
    platform_order_id = fields.Char(string='Platform Order ID')
    odoo_order_id = fields.Many2one('sale.order', string='Odoo Order')
    platform_status = fields.Char(string='Platform Status')
    synced_date = fields.Datetime(string='Synced Date', default=fields.Datetime.now)

    _sql_constraints = [
        ('platform_order_unique', 'unique(platform, platform_order_id)', 
         'Order already mapped!')
    ]


class EcommerceProductMapping(models.Model):
    _name = 'ecommerce.product.mapping'
    _description = 'E-commerce Product Mapping'

    platform = fields.Selection([
        ('shopify', 'Shopify'),
        ('woocommerce', 'WooCommerce'),
        ('amazon', 'Amazon'),
    ], string='Platform')
    platform_product_id = fields.Char(string='Platform Product ID')
    odoo_product_id = fields.Many2one('product.product', string='Odoo Product')
    synced_date = fields.Datetime(string='Synced Date', default=fields.Datetime.now)

    _sql_constraints = [
        ('platform_product_unique', 'unique(platform, platform_product_id)', 
         'Product already mapped!')
    ]