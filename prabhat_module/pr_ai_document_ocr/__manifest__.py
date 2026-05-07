# -*- coding: utf-8 -*-
{
    'name': 'AI Document OCR',
    'version': '18.0.1.0.0',
    'category': 'Document/Document Management',
    'summary': 'Scan documents and extract text using AI/OCR',
    'description': """
AI Document OCR for Odoo 18
=============================

Extract text from images and PDF documents using AI/OCR technology.

Features:
---------
- Upload images and PDF documents
- Extract text using OCR
- Auto-create contacts from business cards
- Auto-create products from invoice images
- Scan purchase orders from images
- Batch document processing
- History of scanned documents
- Support for multiple languages

Requirements:
-------------
- Tesseract OCR engine or Cloud OCR API

For customizations or support:
- Phone/WhatsApp: +91 7982425142
- Email: prabhatshaw24@gmail.com
    """,
    'author': 'Prabhat',
    'website': 'https://shabdprabhat.github.io',
    'depends': ['document', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/ocr_config_views.xml',
        'views/ocr_document_views.xml',
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