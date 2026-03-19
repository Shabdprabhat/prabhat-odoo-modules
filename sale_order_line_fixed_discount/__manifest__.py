# -*- coding: utf-8 -*-
{
    'name': 'Sale Order Line Fixed Discount',
    'version': '18.0.1.0.2',
    'category': 'Sales/Sales',
    'summary': 'Allow fixed amount discounts on sale order lines',
    'description': """
        This module allows users to apply fixed amount discounts on sale order lines
        instead of only percentage-based discounts.

        Features:
        - Add fixed discount amount field on sale order lines
        - Automatic calculation of discount percentage from amount
        - Instant UI updates (discount percentage updates as you type)
        - Integration with invoices
        - Validation to prevent discount exceeding line subtotal
        
        For customizations, contact:
        - Phone/WhatsApp: +91 7982425142 (India)
        - Email: prabhatshaw24@gmail.com
    """,
    'author': 'Prabhat',
    'website': 'https://shabdprabhat.github.io',
    'depends': ['sale_management', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/report_sale_order.xml',
    ],
    # 'web': {
    #     'assets': {
    #         'web.assets_backend': [
    #             'sale_order_line_fixed_discount/static/src/js/discount_amount.js',
    #         ],
    #     },
    # },
    'demo': [],
    'test': [
        'tests/test_discount.py',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
}
