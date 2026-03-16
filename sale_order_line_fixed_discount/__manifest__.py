# -*- coding: utf-8 -*-
{
    'name': 'Sale Order Line Fixed Discount',
    'version': '18.0.1.0.1',
    'category': 'Sales/Sales',
    'summary': 'Allow fixed amount discounts on sale order lines',
    'description': """
        This module allows users to apply fixed amount discounts on sale order lines
        instead of only percentage-based discounts.

        Features:
        - Add fixed discount amount field on sale order lines
        - Automatic calculation of discount percentage from amount
        - Integration with invoices
        - Validation to prevent discount exceeding line subtotal
    """,
    'author': 'Prabhat',
    'website': 'https://github.com/Shabdprabhat/prabhat-odoo-modules',
    'depends': ['sale_management', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/report_sale_order.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
