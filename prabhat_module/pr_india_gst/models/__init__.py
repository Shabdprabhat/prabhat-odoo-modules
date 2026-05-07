# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gstin = fields.Char(string='GSTIN', size=15, help='15-character GSTIN')
    is_gst_applicable = fields.Boolean(string='GST Applicable', default=False)
    
    @api.constrains('gstin')
    def _validate_gstin(self):
        gstin_pattern = re.compile(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$')
        for partner in self:
            if partner.gstin and not gstin_pattern.match(partner.gstin.upper()):
                raise ValidationError('Invalid GSTIN format. Example: 22AAAAA0000A1Z5')


class HSNCode(models.Model):
    _name = 'hsn.code'
    _description = 'HSN Code'
    _order = 'code'

    name = fields.Char(string='HSN Code', required=True, size=8)
    description = fields.Char(string='Description')
    gst_rate = fields.Float(string='GST Rate (%)')
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'HSN Code must be unique!')
    ]


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    hsn_code_id = fields.Many2one('hsn.code', string='HSN Code')
    hsn_code = fields.Char(string='HSN Code (Manual)', size=8)


class AccountMove(models.Model):
    _inherit = 'account.move'

    ewaybill_number = fields.Char(string='E-Way Bill Number', readonly=True)
    ewaybill_date = fields.Date(string='E-Way Bill Date')
    ewaybill_validity = fields.Date(string='E-Way Bill Valid Until')
    transporter_id = fields.Many2one('res.partner', string='Transporter')
    vehicle_number = fields.Char(string='Vehicle Number')
    distance = fields.Integer(string='Distance (km)')
    
    cgst_amount = fields.Monetary(string='CGST', compute='_compute_gst_amounts')
    sgst_amount = fields.Monetary(string='SGST', compute='_compute_gst_amounts')
    igst_amount = fields.Monetary(string='IGST', compute='_compute_gst_amounts')
    cess_amount = fields.Monetary(string='Cess', compute='_compute_gst_amounts')

    @api.depends('invoice_line_ids.tax_ids')
    def _compute_gst_amounts(self):
        for move in self:
            cgst = sgst = igst = cess = 0.0
            for line in move.invoice_line_ids:
                for tax in line.tax_ids:
                    if tax.tax_group_id.name == 'CGST':
                        cgst += line.price_subtotal * tax.amount / 100
                    elif tax.tax_group_id.name == 'SGST':
                        sgst += line.price_subtotal * tax.amount / 100
                    elif tax.tax_group_id.name == 'IGST':
                        igst += line.price_subtotal * tax.amount / 100
                    elif tax.tax_group_id.name == 'Cess':
                        cess += line.price_subtotal * tax.amount / 100
            move.cgst_amount = cgst
            move.sgst_amount = sgst
            move.igst_amount = igst
            move.cess_amount = cess

    def action_generate_ewaybill(self):
        for move in self:
            if not move.partner_id.gstin:
                raise ValidationError('Customer GSTIN is required for E-Way Bill.')
            if not move.partner_id.state_id:
                raise ValidationError('Customer state is required for E-Way Bill.')
            
            eway_num = f"EWB{fields.Date.today().strftime('%Y%m%d')}{move.id:06d}"
            move.write({
                'ewaybill_number': eway_num,
                'ewaybill_date': fields.Date.today(),
                'ewaybill_validity': fields.Date.today() + fields.timedelta(days=72),
            })
            
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'E-Way Bill generated successfully!',
                'type': 'success',
            }
        }


class GSTConfig(models.Model):
    _name = 'gst.config'
    _description = 'GST Configuration'

    name = fields.Char(string='Configuration Name', default='India GST')
    company_id = fields.Many2one('res.company', string='Company', required=True, 
                                 default=lambda self: self.env.company)
    state_id = fields.Many2one('res.country.state', string='Origin State')
    gstin = fields.Char(string='Company GSTIN')
    auto_ewaybill = fields.Boolean(string='Auto Generate E-Way Bill', default=False)
    
    _sql_constraints = [
        ('company_unique', 'unique(company_id)', 'Only one config per company!')
    ]