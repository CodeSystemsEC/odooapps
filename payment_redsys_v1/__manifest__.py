# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Redsys Payment Acquirer',
    'version': '1.0',
    'category': 'Accounting/Payment Acquirers',
    'sequence': -100,
    'summary': 'Payment Acquirer: Redsys Implementation',
    'description': """Redsys Payment Acquirer""",
    'author': "CodeSystems",
    'sequence': -100,
    'website': "http://www.redsys.es",
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',
        'views/payment_redsys_v1_templates.xml',
        'data/payment_provider_data.xml',
    ],
    "external_dependencies": {
        "python3": [
            "pycryptodome",
        ],
    },
    'images': ['static/images/screen_image.png'],
    'application': True,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3',
    'price': 35.00,
    'currency': 'USD'
}
