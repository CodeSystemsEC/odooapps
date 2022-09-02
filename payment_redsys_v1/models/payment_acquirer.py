# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import _, api, fields, models

from werkzeug import urls

from odoo.addons.payment_redsys_v1.const import SUPPORTED_CURRENCIES

_logger = logging.getLogger(__name__)


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(
        selection_add=[('redsys', "Redsys")], ondelete={'redsys': 'set default'})

    redsys_merchant_name = fields.Char(string="Merchant Name", required_if_provider="redsys")
    redsys_merchant_code = fields.Char(string="Merchant code", required_if_provider="redsys")
    redsys_merchant_description = fields.Char(
        string="Product Description", required_if_provider="redsys"
    )
    redsys_secret_key = fields.Char(string="Secret Key", required_if_provider="redsys")
    redsys_terminal = fields.Char(
        string="Terminal", default="1", required_if_provider="redsys"
    )
    redsys_currency = fields.Char(
        string="Currency", default="978", required_if_provider="redsys"
    )
    redsys_transaction_type = fields.Char(
        string="Transtaction Type", default="0", required_if_provider="redsys"
    )
    redsys_merchant_data = fields.Char(string="Merchant Data")
    redsys_merchant_lang = fields.Selection(
        [
            ("001", "Castellano"),
            ("002", "Inglés"),
            ("003", "Catalán"),
            ("004", "Francés"),
            ("005", "Alemán"),
            ("006", "Holandés"),
            ("007", "Italiano"),
            ("008", "Sueco"),
            ("009", "Portugués"),
            ("010", "Valenciano"),
            ("011", "Polaco"),
            ("012", "Gallego"),
            ("013", "Euskera"),
        ],
        string="Merchant Consumer Language",
        default="001",
    )
    redsys_pay_method = fields.Selection(
        [
            ("T", "Pago con Tarjeta"),
            ("R", "Pago por Transferencia"),
            ("D", "Domiciliacion"),
            ("z", "Bizum"),
        ],
        string="Payment Method",
        default="T",
    )
    redsys_signature_version = fields.Selection(
        [("HMAC_SHA256_V1", "HMAC SHA256 V1")], default="HMAC_SHA256_V1"
    )
        
    def _redsys_get_api_url(self):
        """ Return the API URL according to the acquirer state.
        Note: self.ensure_one()
        :return: The API URL
        :rtype: str
        """
        self.ensure_one()

        if self.state == 'enabled':
            return 'https://sis.redsys.es/sis/realizarPago/'
        else:
            return 'https://sis-t.redsys.es:25443/sis/realizarPago/'        

    @api.model
    def _get_compatible_acquirers(self, *args, currency_id=None, **kwargs):
        """ Override of payment to unlist Redsys acquirers when the currency is not supported. """
        acquirers = super()._get_compatible_acquirers(*args, currency_id=currency_id, **kwargs)

        currency = self.env['res.currency'].browse(currency_id).exists()
        if currency and currency.name not in SUPPORTED_CURRENCIES:
            acquirers = acquirers.filtered(lambda a: a.provider != 'redsys')

        return acquirers

    def _get_default_payment_method_id(self):
        self.ensure_one()
        if self.provider != 'redsys':
            return super()._get_default_payment_method_id()
        return self.env.ref('payment_redsys_v1.payment_method_redsys').id

    def redsys_form_generate_values(self, values):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        _logger.info(values)
        _logger.info(base_url)
        values.update({
            "action_url": urls.url_join(base_url, '/payment/redsys/transction/process')
        })

        return values
    
    