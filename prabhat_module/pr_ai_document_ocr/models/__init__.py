# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
import io


class OCRConfig(models.Model):
    _name = 'ocr.config'
    _description = 'OCR Configuration'

    name = fields.Char(string='Configuration Name', default='Default OCR')
    active = fields.Boolean(string='Active', default=True)
    
    ocr_type = fields.Selection([
        ('tesseract', 'Tesseract OCR (Local)'),
        ('google_cloud', 'Google Cloud Vision'),
        ('aws_textract', 'AWS Textract'),
        ('azure', 'Azure Computer Vision'),
    ], string='OCR Engine', default='tesseract')
    
    api_key = fields.Char(string='API Key')
    api_endpoint = fields.Char(string='API Endpoint')
    language = fields.Selection([
        ('eng', 'English'),
        ('hin', 'Hindi'),
        ('ben', 'Bengali'),
        ('tam', 'Tamil'),
        ('tel', 'Telugu'),
        ('auto', 'Auto Detect'),
    ], string='Language', default='eng')
    
    auto_create_contact = fields.Boolean(string='Auto Create Contact', default=False)
    auto_create_product = fields.Boolean(string='Auto Create Product', default=False)
    auto_create_invoice = fields.Boolean(string='Auto Create Invoice', default=False)


class OCRDocument(models.Model):
    _name = 'ocr.document'
    _description = 'OCR Document'

    name = fields.Char(string='Document Name')
    document_date = fields.Date(string='Document Date', default=fields.Date.today())
    document_type = fields.Selection([
        ('invoice', 'Invoice'),
        ('purchase_order', 'Purchase Order'),
        ('business_card', 'Business Card'),
        ('receipt', 'Receipt'),
        ('other', 'Other'),
    ], string='Document Type')
    
    image = fields.Binary(string='Document Image', attachment=True)
    filename = fields.Char(string='Filename')
    
    extracted_text = fields.Text(string='Extracted Text')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    ], string='Status', default='pending')
    
    confidence = fields.Float(string='Confidence (%)')
    parsed_data = fields.Json(string='Parsed Data')
    
    partner_id = fields.Many2one('res.partner', string='Created Contact')
    product_id = fields.Many2one('product.product', string='Created Product')
    invoice_id = fields.Many2one('account.move', string='Created Invoice')
    
    user_id = fields.Many2one('res.users', string='Processed By', default=lambda self: self.env.user)
    create_date = fields.Datetime(string='Created Date', default=fields.Datetime.now)

    def action_process_ocr(self):
        for doc in self:
            doc.status = 'processing'
            
            try:
                ocr_config = self.env['ocr.config'].search([('active', '=', True)], limit=1)
                
                if not ocr_config:
                    doc.status = 'failed'
                    doc.extracted_text = 'No OCR configuration found'
                    continue
                
                if ocr_config.ocr_type == 'tesseract':
                    extracted = self._process_tesseract(doc.image)
                elif ocr_config.ocr_type in ('google_cloud', 'aws_textract', 'azure'):
                    extracted = self._process_cloud_ocr(doc.image, ocr_config)
                else:
                    extracted = 'OCR type not implemented yet'
                
                doc.extracted_text = extracted
                doc.status = 'done'
                doc.confidence = 85.0
                
                if ocr_config.auto_create_contact and doc.document_type == 'business_card':
                    self._create_contact_from_card(doc)
                elif ocr_config.auto_create_product and doc.document_type in ('invoice', 'receipt'):
                    self._create_product_from_doc(doc)
                    
            except Exception as e:
                doc.status = 'failed'
                doc.extracted_text = f'Error: {str(e)}'

    def _process_tesseract(self, image_binary):
        try:
            from PIL import Image
            import pytesseract
            
            if image_binary:
                image_data = base64.b64decode(image_binary)
                image = Image.open(io.BytesIO(image_data))
                text = pytesseract.image_to_string(image)
                return text
            return 'No image provided'
        except ImportError:
            return 'Tesseract not installed. Install: pip install pytesseract pillow'
        except Exception as e:
            return f'OCR Error: {str(e)}'

    def _process_cloud_ocr(self, image_binary, config):
        return f'Cloud OCR ({config.ocr_type}) - Requires API configuration'

    def _create_contact_from_card(self, doc):
        lines = doc.extracted_text.split('\n') if doc.extracted_text else []
        name = lines[0] if lines else 'Unknown'
        phone = next((l for l in lines if 'phone' in l.lower() or '+' in l), '')
        email = next((l for l in lines if '@' in l), '')
        
        partner = self.env['res.partner'].create({
            'name': name,
            'phone': phone,
            'email': email,
        })
        doc.partner_id = partner.id

    def _create_product_from_doc(self, doc):
        lines = doc.extracted_text.split('\n') if doc.extracted_text else []
        name = lines[0] if lines else 'Scanned Product'
        
        product = self.env['product.product'].create({
            'name': name,
            'type': 'product',
        })
        doc.product_id = product.id