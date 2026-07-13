# -*- coding: utf-8 -*-
# Copyright 2024-2026 Prabhat
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    'name': 'PackMate Product Bundle',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Create and sell product bundles, combo packs, and sales kits from quotations.',
    'description': """
PackMate helps sales teams sell product bundles, combo packs, and sales kits in Odoo.

Features:
- Mark a product as a PackMate kit.
- Add kit component products with quantities.
- Manual or automatic kit sales price calculation.
- Manual or automatic kit cost calculation.
- Add kit lines on sale quotations.
- Expand kit components as priced sale lines before confirmation.
- Use standard Odoo delivery flow for the real component products.
    """,
    'author': 'Prabhat',
    'website': 'https://shabdprabhat.github.io',
    'depends': [
        'sale',
        'sale_stock',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/packmate_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
}
