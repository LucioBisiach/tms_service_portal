# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'TMS Services Portal',
    'version': '1.0',
    'category': 'Info Supplier',
    'depends': ['portal','tms'],
    'data': [
        'views/portal_view.xml',
        'views/res_users_view.xml'
        #'security/ir.model.access.csv',

    ],
    'demo': [
        ],
    'css': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
