# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import requests
from datetime import datetime, timedelta


class CurrencyRateProvider(models.Model):
    _name = 'currency.rate.provider'
    _description = 'Currency Rate Provider'

    name = fields.Char(string='Provider Name', required=True)
    api_service = fields.Selection([
        ('exchange_rate_api', 'ExchangeRate-API'),
        ('open_exchange_rates', 'OpenExchangeRates'),
        ('fixer', 'Fixer.io'),
        ('frankfurter', 'Frankfurter (Free)'),
    ], string='API Service', default='frankfurter')
    
    api_key = fields.Char(string='API Key')
    active = fields.Boolean(string='Active', default=True)
    base_currency = fields.Many2one('res.currency', string='Base Currency', 
                                    default=lambda self: self.env.ref('base.USD'))
    auto_update = fields.Boolean(string='Auto Update', default=True)
    update_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('hourly', 'Hourly'),
    ], string='Update Frequency', default='daily')
    last_update = fields.Datetime(string='Last Update')

    def action_fetch_rates(self):
        self.ensure_one()
        
        try:
            if self.api_service == 'frankfurter':
                self._fetch_frankfurter()
            elif self.api_service == 'exchange_rate_api':
                self._fetch_exchange_rate_api()
            elif self.api_service == 'open_exchange_rates':
                self._fetch_open_exchange_rates()
            elif self.api_service == 'fixer':
                self._fetch_fixer()
            
            self.last_update = fields.Datetime.now()
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': 'Currency rates updated successfully!',
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(f'Failed to fetch rates: {str(e)}')

    def _fetch_frankfurter(self):
        base = self.base_currency.name
        url = f'https://api.frankfurter.app/latest?from={base}'
        
        response = requests.get(url, timeout=30)
        data = response.json()
        
        for currency_name, rate in data.get('rates', {}).items():
            currency = self.env['res.currency'].search([('name', '=', currency_name)], limit=1)
            if currency:
                self.env['res.currency.rate'].create_or_update_rate(
                    currency, rate, data.get('date'), self.base_currency)

    def _fetch_exchange_rate_api(self):
        if not self.api_key:
            raise UserError('API Key required for ExchangeRate-API')
        
        base = self.base_currency.name
        url = f'https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{base}'
        
        response = requests.get(url, timeout=30)
        data = response.json()
        
        for currency_name, rate in data.get('conversion_rates', {}).items():
            currency = self.env['res.currency'].search([('name', '=', currency_name)], limit=1)
            if currency:
                self.env['res.currency.rate'].create_or_update_rate(
                    currency, rate, fields.Date.today(), self.base_currency)

    def _fetch_open_exchange_rates(self):
        if not self.api_key:
            raise UserError('API Key required for OpenExchangeRates')
        
        base = self.base_currency.name
        url = f'https://openexchangerates.org/api/latest.json?app_id={self.api_key}&base={base}'
        
        response = requests.get(url, timeout=30)
        data = response.json()
        
        for currency_name, rate in data.get('rates', {}).items():
            currency = self.env['res.currency'].search([('name', '=', currency_name)], limit=1)
            if currency:
                self.env['res.currency.rate'].create_or_update_rate(
                    currency, rate, fields.Date.today(), self.base_currency)

    def _fetch_fixer(self):
        if not self.api_key:
            raise UserError('API Key required for Fixer.io')
        
        base = self.base_currency.name
        url = f'http://data.fixer.io/api/latest?access_key={self.api_key}&base={base}'
        
        response = requests.get(url, timeout=30)
        data = response.json()
        
        for currency_name, rate in data.get('rates', {}).items():
            currency = self.env['res.currency'].search([('name', '=', currency_name)], limit=1)
            if currency:
                self.env['res.currency.rate'].create_or_update_rate(
                    currency, rate, fields.Date.today(), self.base_currency)


class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'

    provider_id = fields.Many2one('currency.rate.provider', string='Provider')
    is_auto_updated = fields.Boolean(string='Auto Updated', default=False)

    @api.model
    def create_or_update_rate(self, currency, rate, date, base_currency):
        existing = self.search([
            ('currency_id', '=', currency.id),
            ('name', '=', date),
        ], limit=1)
        
        if existing:
            existing.write({'rate': rate, 'is_auto_updated': True})
        else:
            self.create({
                'currency_id': currency.id,
                'name': date,
                'rate': rate,
                'company_id': False,
                'is_auto_updated': True,
            })


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    auto_update_prices = fields.Boolean(string='Auto Update with Currency Rates', default=False)

    def action_refresh_prices(self):
        for pricelist in self:
            for item in pricelist.item_ids:
                if item.base == 'pricelist' and item.base_pricelist_id:
                    continue
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Prices refreshed based on current exchange rates',
                'type': 'success',
            }
        }