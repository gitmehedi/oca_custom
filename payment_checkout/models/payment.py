# coding: utf-8

import logging
import requests

from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)

# Force the API version to avoid breaking in case of update on Checkout side
# cf https://checkout.com/docs/api#versioning
# changelog https://checkout.com/docs/upgrades#api-changelog
CHECKOUT_HEADERS = {'Checkout-Version': '2016-03-07'}

# The following currencies are integer only, see https://checkout.com/docs/currencies#zero-decimal
INT_CURRENCIES = [
    u'BIF', u'XAF', u'XPF', u'CLP', u'KMF', u'DJF', u'GNF', u'JPY', u'MGA', u'PYGí', u'RWF', u'KRW',
    u'VUV', u'VND', u'XOF'
];


class PaymentAcquirerCheckout(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('checkout', 'Checkout')])
    checkout_secret_key = fields.Char(required_if_provider='checkout', groups='base.group_user')
    checkout_publishable_key = fields.Char(required_if_provider='checkout', groups='base.group_user')
    checkout_image_url = fields.Char(
        "Checkout Image URL", groups='base.group_user',
        help="A relative or absolute URL pointing to a square image of your "
             "brand or product. As defined in your Checkout profile. See: "
             "https://docs.checkout.com/getting-started/introduction")

    @api.multi
    def checkout_form_generate_values(self, tx_values):
        self.ensure_one()
        checkout_tx_values = dict(tx_values)
        temp_checkout_tx_values = {
            'company': self.company_id.name,
            'amount': tx_values.get('amount'),
            'currency': tx_values.get('currency') and tx_values.get('currency').name or '',
            'currency_id': tx_values.get('currency') and tx_values.get('currency').id or '',
            'address_line1': tx_values['partner_address'],
            'address_city': tx_values['partner_city'],
            'address_country': tx_values['partner_country'] and tx_values['partner_country'].name or '',
            'email': tx_values['partner_email'],
            'address_zip': tx_values['partner_zip'],
            'name': tx_values['partner_name'],
            'phone': tx_values['partner_phone'],
        }

        temp_checkout_tx_values['returndata'] = checkout_tx_values.pop('return_url', '')
        checkout_tx_values.update(temp_checkout_tx_values)
        return checkout_tx_values

    @api.model
    def _get_checkout_api_url(self):
        return 'sandbox.checkout.com/api2/v2'

    @api.model
    def checkout_s2s_form_process(self, data):
        payment_token = self.env['payment.token'].sudo().create({
            'cc_number': data['cc_number'],
            'cc_holder_name': data['cc_holder_name'],
            'cc_expiry': data['cc_expiry'],
            'cc_brand': data['cc_brand'],
            'cvc': data['cvc'],
            'acquirer_id': int(data['acquirer_id']),
            'partner_id': int(data['partner_id'])
        })
        return payment_token.id

    @api.multi
    def checkout_s2s_form_validate(self, data):
        self.ensure_one()

        # mandatory fields
        for field_name in ["cc_number", "cvc", "cc_holder_name", "cc_expiry", "cc_brand"]:
            if not data.get(field_name):
                return False
        return True


class PaymentTransactionCheckout(models.Model):
    _inherit = 'payment.transaction'

    def _create_checkout_charge(self, acquirer_ref=None, tokenid=None, email=None):
        api_url_charge = 'https://%s/charges' % (self.acquirer_id._get_checkout_api_url())
        charge_params = {
            'amount': int(self.amount if self.currency_id.name in INT_CURRENCIES else self.amount*100),
            'currency': self.currency_id.name,
            'metadata[reference]': self.reference
        }
        if acquirer_ref:
            charge_params['customer'] = acquirer_ref
        if tokenid:
            charge_params['card'] = str(tokenid)
        if email:
            charge_params['receipt_email'] = email
        r = requests.post(api_url_charge,
                          auth=(self.acquirer_id.checkout_secret_key, ''),
                          params=charge_params,
                          headers=CHECKOUT_HEADERS)
        return r.json()

    @api.multi
    def checkout_s2s_do_transaction(self, **kwargs):
        self.ensure_one()
        result = self._create_checkout_charge(acquirer_ref=self.payment_token_id.acquirer_ref)
        return self._checkout_s2s_validate_tree(result)

    @api.model
    def _checkout_form_get_tx_from_data(self, data):
        """ Given a data dict coming from checkout, verify it and find the related
        transaction record. """
        reference = data.get('metadata', {}).get('reference')
        if not reference:
            error_msg = _(
                'Checkout: invalid reply received from provider, missing reference. Additional message: %s'
                % data.get('error', {}).get('message', '')
            )
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        tx = self.search([('reference', '=', reference)])
        if not tx:
            error_msg = (_('Checkout: no order found for reference %s') % reference)
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        elif len(tx) > 1:
            error_msg = (_('Checkout: %s orders found for reference %s') % (len(tx), reference))
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        return tx[0]

    @api.multi
    def _checkout_s2s_validate_tree(self, tree):
        self.ensure_one()
        if self.state not in ('draft', 'pending'):
            _logger.info('Checkout: trying to validate an already validated tx (ref %s)', self.reference)
            return True

        status = tree.get('status')
        if status == 'succeeded':
            self.write({
                'state': 'done',
                'date_validate': fields.datetime.now(),
                'acquirer_reference': tree.get('id'),
            })
            if self.sudo().callback_eval:
                safe_eval(self.sudo().callback_eval, {'self': self})
            return True
        else:
            error = tree['error']['message']
            _logger.warn(error)
            self.sudo().write({
                'state': 'error',
                'state_message': error,
                'acquirer_reference': tree.get('id'),
                'date_validate': fields.datetime.now(),
            })
            return False

    @api.multi
    def _checkout_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        reference = data['metadata']['reference']
        if reference != self.reference:
            invalid_parameters.append(('Reference', reference, self.reference))
        return invalid_parameters

    @api.multi
    def _checkout_form_validate(self,  data):
        return self._checkout_s2s_validate_tree(data)


class PaymentTokenCheckout(models.Model):
    _inherit = 'payment.token'

    @api.model
    def checkout_create(self, values):
        res = {}
        payment_acquirer = self.env['payment.acquirer'].browse(values.get('acquirer_id'))
        url_token = 'https://%s/charges/token' % payment_acquirer._get_checkout_api_url()
        url_customer = 'https://%s/customers' % payment_acquirer._get_checkout_api_url()
        if values.get('cc_number'):
            payment_params = {
                'card[number]': values['cc_number'].replace(' ', ''),
                'card[exp_month]': str(values['cc_expiry'][:2]),
                'card[exp_year]': str(values['cc_expiry'][-2:]),
                'card[cvc]': values['cvc'],
            }
            r = requests.post(url_token,
                              auth=(payment_acquirer.checkout_secret_key, ''),
                              params=payment_params,
                              headers=CHECKOUT_HEADERS)
            token = r.json()
            if token.get('id'):
                customer_params = {
                    'source': token['id']
                }
                r = requests.post(url_customer,
                                  auth=(payment_acquirer.checkout_secret_key, ''),
                                  params=customer_params,
                                  headers=CHECKOUT_HEADERS)
                customer = r.json()
                res = {
                    'acquirer_ref': customer['id'],
                    'name': 'XXXXXXXXXXXX%s - %s' % (values['cc_number'][-4:], values['cc_holder_name'])
                }
            elif token.get('error'):
                raise UserError(token['error']['message'])

        # pop credit card info to info sent to create
        for field_name in ["cc_number", "cvc", "cc_holder_name", "cc_expiry", "cc_brand"]:
            values.pop(field_name, None)
        return res
