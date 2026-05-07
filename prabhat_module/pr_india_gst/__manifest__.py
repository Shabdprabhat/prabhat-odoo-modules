# -*- coding: utf-8 -*-
{
    'name': 'India GST & E-Way Bill',
    'version': '18.0.1.0.0',
    'category': 'Accounting/India',
    'summary': 'GST compliance and E-Way Bill generation for India',
    'description': """
India GST & E-Way Bill Module for Odoo 18
=========================================

This module provides Indian GST compliance features and E-Way Bill generation.

Features:
---------
- GSTIN validation for partners
- HSN Code validation
- GST tax rate configuration (CGST, SGST, IGST)
- E-Way Bill generation for invoices
- E-Way Bill print format
- GST TDS/TCS support
-GST invoice format as per government requirements

Requirements:
-------------
- India localization module installed

For customizations or support:
- Phone/WhatsApp: +91 7982425142
- Email: prabhatshaw24@gmail.com
    """,
    'author': 'Prabhat',
    'website': 'https://shabdprabhat.github.io',
    'depends': ['account', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
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