# -*- coding: utf-8 -*-
{
    'name': "Prospects Dashboard",

    'summary': """
      Dashboard Prospects - For marketing and accelerator """,

    'description': """

    """,

    'author': "OTB Africa",
    'website': "http://www.otbafrica.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'help',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project'],

    # always loaded
    'data': [
        'views/investor_res_id.xml',
        'views/investor_dashboard.xml',
        'views/investors.xml',
        'views/assets.xml'

    ],
    'qweb': [
        "static/src/xml/investors_templates.xml",

    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
