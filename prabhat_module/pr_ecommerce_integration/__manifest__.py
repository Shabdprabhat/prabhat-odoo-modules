# -*- coding: utf-8 -*-
{
    'name': 'E-commerce Integration',
    'version': '18.0.1.0.0',
    'category': 'Website/E-commerce',
    'summary': 'Connect Odoo with Shopify, WooCommerce, Amazon',
    'description': """
E-commerce Integration for Odoo 18
===================================

Connect your Odoo with popular e-commerce platforms.

Features:
---------
- Shopify integration
- WooCommerce integration
- Amazon Seller Central integration
- Sync products from e-commerce to Odoo
- Sync orders from e-commerce to Odoo
- Sync inventory/stock levels
- Auto-create customers
- Order status sync

Requirements:
-------------
- API credentials from respective platform

For customizations or support:
- Phone/WhatsApp: +91 7982425142
- Email: prabhatshaw24@gmail.com
    """,
    'author': 'Prabhat',
    'website': 'https://shabdprabhat.github.io',
    'depends': ['sale', 'product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/ecommerce_config_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
}