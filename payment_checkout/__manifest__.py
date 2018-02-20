# -*- coding: utf-8 -*-

{
    'name': 'Checkout Payment Acquirer',
    'category': 'Payment',
    'summary': 'Payment Acquirer: Checkout Implementation',
    'version': '1.0',
    'description': """Checkout Payment Acquirer""",
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',
        'views/payment_checkout_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
}
