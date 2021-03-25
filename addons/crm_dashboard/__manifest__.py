# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo,RDB Dashboard for CRM
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "CRM Dashboard",

    'summary': """
        Dashboard For CRM managers and Officers.
        """,

    'description': """
        Dashboard which includes Projects, Tasks, Inquiries and Companies information including All register contacts,Leads etc
    """,

    'author': "Hilar AK,Boniface Irungu(OTBAfrica)",
    'website': "https://www.linkedin.com/in/hilar-ak/,www.otbafrica.com",
    'category': "Generic Modules/Human Resources",
    'version': "11.0.1.0.0",
    'depends': [
        'base','mail'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/crm_dashboard.xml',
    ],
    'qweb': [
        "static/src/xml/crm_dashboard.xml",
    ],
    'images': ["static/description/banner.gif"],
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
