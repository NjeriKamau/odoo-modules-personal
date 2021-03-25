# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo.tools.translate import _
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from odoo import tools, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
from odoo.osv import  osv
from odoo import SUPERUSER_ID

class ExtendProjectTask(models.Model):
    _inherit = 'project.task'

    # lead_id = fields.Many2one('crm.lead', string='Task Link')
    priority = fields.Selection([
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),], default='0', index=True, string="Priority")
    lead_ids = fields.Many2many('crm.lead', string="Investment Link", relation='crm_lead_task_link', column1='task_id', column2='lead_id')

class ExtendProjectTags(models.Model):
    _inherit = 'project.tags'

    investor_ids = fields.Many2one('crm.lead', string='Investor Link')

class ExtendResUser(models.Model):
    _inherit = 'res.users'

    investor_ids = fields.Many2one('crm.lead', string='Investor Link')

class ExtendCompany(models.Model):
    _inherit = 'res.partner'

    is_primary =  fields.Boolean(string='Primary Contact')


    @api.model
    def save_company_from_investor(self, vals):

        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def create(self, vals):
        entity = super(ExtendCompany, self).create(vals)
        company_stage = self.env['crm.stage'].search([('is_company', '=', True)]).id

        for investor in entity.x_investor_count_ids:
            if investor.project_count >= 1:
                investor.update({'stage_id': company_stage})

        return entity

    @api.multi
    def write(self, vals):
        entity = super(ExtendCompany, self).write(vals)
        if not vals.get('x_investor_count_ids', False):
            return entity

        ids = vals.get('x_investor_count_ids')[0][2]
        company_stage = self.env['crm.stage'].search([('is_company','=',True)]).id

        for investor in self.env['crm.lead'].browse(ids):
            if investor.project_count >= 1:
                investor.update({'stage_id':company_stage})

        return entity


class ExtendProjectInv(models.Model):
    _inherit = 'project.project'

    @api.model
    def save_project_from_investor(self, vals):

        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def create(self, vals):
        entity = super(ExtendProjectInv, self).create(vals)
        # print("Inside Project Investor Create")
        if not vals.get('investor_ids', False):
            try:
                return entity
            except:
                raise ValidationError(_(
                        'Sorry, this record cannot be saved.'))
        # print("Inside Create Project Investor=======================")

        ids = entity.investor_ids.ids
        # print(ids)
        # print(entity.investor_ids.ids)
        # print("vals.get('investor_ids')[0][2]+++++++++++++++______________")
        project_stage = self.env['crm.stage'].search([('is_project', '=', True)]).id

        for investor in self.env['crm.lead'].browse(ids):
            investor.update({'stage_id': project_stage})
        # print("Inside Create Project Investor after for loop0000000000000000000-----------------")

        return entity


    @api.multi
    def write(self, vals):
        entity = super(ExtendProjectInv, self).write(vals)
        if not vals.get('investor_ids', False):
            return entity

        ids = vals.get('investor_ids')[0][2]
        project_stage = self.env['crm.stage'].search([('is_project','=',True)]).id
        for investor in self.env['crm.lead'].browse(ids):
            investor.update({'stage_id': project_stage})


        return entity


class ActivityExtend(models.Model):
    _inherit = "mail.activity"


    @api.multi
    def action_create_calendar_event(self):
        self.ensure_one()
        investor_meeting = self.env['crm.lead']
        action = self.env.ref('calendar.action_calendar_event').read()[0]
        partner_ids = self.env.user.partner_id.ids

        if investor_meeting:
            for investor in investor_meeting.contact_info:
                partner_ids.append(investor.id)
                action['context'] = {
                    'default_opportunity_id': self.id if self.type == 'opportunity' else False,
                    'default_partner_id': self.partner_id.id,
                    'default_partner_ids': partner_ids,
                    'default_team_id': self.team_id.id,
                    'default_name': self.name,
                }
                return action
        else:
            action['context'] = {
                'default_partner_ids': partner_ids,
                # 'default_partner_id': self.partner_id.id,
                'default_activity_type_id': self.activity_type_id.id,
                'default_res_id': self.env.context.get('default_res_id'),
                'default_res_model': self.env.context.get('default_res_model'),
                'default_name': self.summary,
                'default_description': self.note and tools.html2plaintext(self.note).strip() or '',
                'default_activity_ids': [(6, 0, self.ids)],
            }
            return action

class ProjectTaskExtend(models.Model):
    _inherit='project.task'

    lead_id =  fields.Many2one('crm.lead', 'Opportunity')


class DocumentExtend(models.Model):
    _inherit = 'muk_dms.file'

    prospect_document = fields.Many2one(comodel_name='crm.lead', string='Partner')

class InvestorSource(models.Model):
    _name = 'investor.source'
    _inherit = ['mail.thread']

    name = fields.Char(string='Source Name')
    is_referral = fields.Boolean(string='This is a Referral', help='Select this field if the source is referral, this will enable the visibility of a field')
    is_conference = fields.Boolean(string='This is a Conference', help='Select this field if the source is conference, this will enable the visibility of a field')

class InvestorReftype(models.Model):
    _name = 'investor.reftype'
    _inherit = ['mail.thread']

    name = fields.Char(string='Referral Type')
    # is_referral = fields.Boolean(string='This is a referral', help = 'Select this field if the source is referral')
