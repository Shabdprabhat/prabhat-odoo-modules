# -*- coding: utf-8 -*-
{
    'name': 'Barcode Scanner by Camera',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Stock',
    'summary': 'Scan barcodes using phone camera in sale and purchase',
    'description': """
Barcode Scanner by Camera for Odoo 18
======================================

Scan barcodes directly using your phone camera in Sale Order and Purchase Order.

Features:
---------
- Scan barcodes using device camera
- Add products to sale order by scanning
- Add products to purchase order by scanning
- Quick product search in orders
- Works on mobile and desktop with camera
- Support for multiple barcode formats (EAN, UPC, QR)

Requirements:
-------------
- Camera access on device

For customizations or support:
- Phone/WhatsApp: +91 7982425142
- Email: prabhatshaw24@gmail.com
    """,
    'author': 'Prabhat',
    'website': 'https://shabdprabhat.github.io',
    'depends': ['sale', 'purchase', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
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
    'web': {
        'assets': {
            'web.assets_backend': [
                'pr_barcode_scanner_camera/static/src/js/barcode_scanner.js',
            ],
        },
    },
}