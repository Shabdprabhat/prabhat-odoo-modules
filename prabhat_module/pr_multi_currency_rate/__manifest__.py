# -*- coding: utf-8 -*-
{
    'name': 'Multi-Currency Live Rates',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Currencies',
    'summary': 'Auto-update exchange rates from live APIs',
    'description': """
Multi-Currency Live Rates for Odoo 18
======================================

Automatically fetch and update currency exchange rates from live APIs.

Features:
---------
- Live exchange rate fetching
- Auto-update currency rates daily
- Manual refresh option
- Historical rate tracking
- API: ExchangeRate-API, OpenExchangeRates, Fixer.io support
- Apply to price lists automatically

Requirements:
-------------
- Active internet connection

For customizations or support:
- Phone/WhatsApp: +91 7982425142
- Email: prabhatshaw24@gmail.com
    """,
    'author': 'Prabhat',
    'website': 'https://shabdprabhat.github.io',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_currency_views.xml',
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