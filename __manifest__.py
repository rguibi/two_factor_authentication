# -*- coding: utf-8 -*-


{
    'name': 'Two Factor Authentication',
    'category': 'system',
    'version': '13.0.2.2',
    'author': 'ERP Labz',
    'website': 'erplabz.com',
    #"live_test_url" :  "https://2fa.erplabz.com/web/login",
    'summary': "Provide extra layer of security using Google Time Based OTP (TOTP), Authentication By Authenticator Google, Google Authenticator, 2FA",
    'license': 'OPL-1',
    'description':
        """
Provide extra layer of security using Google Time Based OTP (TOTP). Two Step Authentication
google authentication,
google 2fa,
odoo 2fa,
odoo login 2fa,
2nd factor authentication,
2fa odoo,
odoo otp,
odoo login otp,
login otp odoo,
odoo google auth,
google authenticator odoo,
odoo google authenticator,
google authenticator,
otp,
one time password,
- This module required external_dependencies: python library 'qrcode' installed
========================

        """,
    'depends': ['web', 'mail', 'auth_signup'],
    'auto_install': False,
    'data': [
            'views/res_users_view_inherit.xml',
            'views/template.xml',
            'data/email_template.xml',
            ],
    'external_dependencies': {
        'python' : ['qrcode'],
    },
    "images":['static/description/Banner.png'],
	    

    'currency': 'EUR',
    'price': 30.00,



}
