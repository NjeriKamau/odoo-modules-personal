# -*- coding: utf-8 -*-

{
    'name': 'Prospect Pre-establishment',
    'summary': 'This app allows Prospects to connect with RDB',

    'description': """
        This is a custom Prospect relationship management module for the RDB by OTB Africa Ltd.

    """,
    'author': "OTB Africa",
    'website': "http://www.otbafrica.com",
    'category': 'Random',
    'sequence': 900,
    'version': '1.0',
    # 'depends': [
    #     'base', 'website', 'crm','website_crm', 'hr', 'project', 'bi_crm_task',
    #     'muk_dms', 'calendar', 'investors_dashboard'
    # ],
    'depends': [
        'base', 'crm', 'project','muk_dms', 'calendar','res_partner_addons'],
    # 'depends': ['base', 'crm', 'hr', 'project','project_extend', 'muk_dms', 'calendar'],
    'data': [
        'views/backend/misc/assets.xml',
        'security/investor_security.xml',
        'security/ir.model.access.csv',

        'data/crm_data.xml',
        'data/crm_stage_data.xml',
        'data/crm_lead_data.xml',
        'data/mail_template_data.xml',

        # 'wizard/investor_lost_views.xml',

        # 'views/frontend/website_crm.xml',
        # 'views/frontend/theme.xml',

        'views/backend/misc/res_partner_form.xml',
        # 'views/backend/misc/crm_investor_project_link.xml',
        # 'views/backend/misc/add_contact_form.xml',
        # 'views/backend/misc/crm_inquiry.xml',
        'views/backend/misc/crm_stages_extend.xml',
        'views/backend/misc/investor_source.xml',
        'views/backend/misc/referral_type.xml',


        'views/backend/leads/leads_replace.xml',
        'views/backend/leads/leads_action_replace.xml',

        'views/backend/opportunities/opportunity_replace.xml',
        'views/backend/opportunities/opp_action_replace.xml',
        'views/backend/opportunities/opp_simple_replace.xml',

        'views/backend/misc/menuitems.xml',

    ],
    'images': ['static/src/img/icon.png'],
    'application': True,
    'auto_install': False,
    'license': "AGPL-3",

}



                                                                                                                                                # Njeri, Ken and Bonnie was here
