# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo.tools.translate import _
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from odoo import tools, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo import api, fields, models, _
import logging
from odoo.osv import  osv
from odoo import SUPERUSER_ID



class crm_inquiry(models.Model):
    
    _name = 'crm.inquiry'
    _inherit = ["crm.lead",]
    _order = 'id'


    name = fields.Many2one('project.project', string="Projects Name")


    matched_company = fields.Many2one('res.company')
    validated = fields.Boolean(default=False)
    point_of_entry = fields.Many2one('entry.point')
    type_of_interaction = fields.Many2one('interaction.type', required=True)
    # special information page(Tab)
    x_project_likelihood = fields.Char('Project Likelihood')
    x_project_amount = fields.Char('Project Amount')
    x_project_timing = fields.Char('Project Timing')
    x_project_jobs_offered = fields.Char('Jobs Offered by Project')

    x_investor_performancedata = fields.Char('Prospect Performance Data')
    x_investor_shareholding = fields.Char('Prospect Shareholding')

    # child_ids = fields.Many2many('res.partner', string='Contacts', domain=[
    #     ('active', '=', True)], required=True)
    cert = fields.Char('CERT',required=True)
    tin = fields.Char('TIN', required=True)

    @api.multi
    def validate(self):
        if self.matched_company:
            self.validated = True
            self.env['crm.lead'].create({
                'itype': self.itype,
                'cert': self.cert,
                'tin': self.tin,
                'type_invest': self.type_invest.id,
                'project_description': self.project_description,
                'start_date': self.start_date,
                'investment_amount': self.investment_amount,
                'p_job_creation': self.p_job_creation,
                'p_address': self.p_address,
                'sector': self.sector,
                'city': self.city,
                'state_id': self.state_id,
                'partner_name': self.matched_company.id,
                'title': self.title.id,
                'contact_name': self.contact_name,
                'function': self.function,
                'email_from': self.email_from,
                'phone': self.phone,
                'sector': self.sector.id,
                'name': self.name,
                'country_id': self.country_id.id,
                'user_id': self.user_id.id
            })
        else:
            raise osv.except_osv(('Error'), ('You need to select a matched company to validate this request'))


    # @api.multi
    # @api.depends('partner_name')
    # def name_get(self):
    #     res = []
    #     for record in self:
    #         res.append((record.id, "%s " % (record.partner_name.name)))
    #     return res