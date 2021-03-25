 #-*- coding: utf-8 -*-
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
# from PIL import Image
# from PIL import ImageEnhance

# class PartnerIndustry(models.Model):
#     _inherit = 'res.partner.industry'

    # x_sub_sector = fields.One2many(comodel_name='res.partner.sub_sector', inverse_name='x_industry', string='Sub Sector')

class crm_lead(models.Model):
    #create lead
    # @api.multi
    # def create_project_view(self):
    #     if self.project_id.id:
    #         entity = self.env['project.project'].search([('id', '=', self.project_id.id)], limit=1)
    #     else:
    #         entity = self.env['project.project'].create({
    #             'name': self.name,
    #             'investor_ids':self.project_ids
    #         })
    #         self.write({
    #             'project_id': entity.id,
    #             'project_ids':[(4, entity.id)]
    #         })


    #     form_context = {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Edit Project Details',
    #         'res_model': 'project.project',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'view_id': self.env.ref('investor_contact.investor_project_edit_link', False).id,
    #         'res_id': entity.id,
    #         'target': 'new',
    #         'context': {
    #             'default_modal_view': True,
    #             'default_name': self.name,
    #             'default_investor_id': self.id,
    #             'default_investor_ids':[(4, self.id)],
    #             'default_x_state': 'prospective',
    #         }
    #     }
    #     reload_context =  {
    #         'type': 'ir.actions.client',
    #         'tag': 'reload',
    #     }
    #     return form_context

    @api.multi
    def create_request(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create a Request',
            'res_model': 'website.support.ticket',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'view_id': self.env.ref('website_support.website_support_ticket_view_form').id,
            'context': {
                'default_investor_ids': [self.id]
            },
        }



    @api.multi
    def project_tasks_open_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create a Task',
            'res_model': 'project.task',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'view_id': self.env.ref('project_extend.project_task_custom_form_view').id,
            'context': {
                # 'default_modal_view': True,
                # 'default_name': 'Task for ' + str(self.name),
                'default_lead_id': self.id,
                'default_lead_ids': [(4, self.id)]

            },
        }
    @api.multi
    def project_tasks_dashboard_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create a Task',
            'res_model': 'project.task',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'view_id': self.env.ref('project_extend.project_task_custom_form_view').id,
        }


    """ CRM Lead Case """
    _name = 'crm.lead'
    _description = "Prospects"
    _inherit = ['mail.thread', 'crm.lead']
    # _inherits = {'res.partner': 'department_name'}
    _order = 'id'


    def logged_user_initials(self):
        fullname = self.env.user.name
        initials = ''.join([x[0].upper() for x in fullname.split(' ')])
        # print("User Initials >>>>>")
        # print(fullname)
        return initials

    def _get_default_favorite_user_ids(self):
        return [(6, 0, [self.env.uid])]


    @api.multi
    def investor_create_projects_view(self):
        project_stage = self.env['crm.stage'].search([('is_project','=',True)]).id

        self.update({'stage_id':project_stage})

        return {
            'type': 'ir.actions.act_window_close',
            'name': 'Project Details',
            'res_model': 'project.project',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'tag':'reload',
            'view_id': self.env.ref('investor_contact.investor_project_edit_link').id,
            'context': {
                'default_name': self.name,
                # include description
                # 'default_project_description':self.describe,
                'default_investor_id': self.id,
                'default_investor_ids':[(4, self.id)],
                'default_x_state': 'prospective',
            }

        }


    def _default_stage_id_custom(self):
        return self.env['crm.stage'].search(
            [('id', '!=', False)],
            order='sequence asc',
            limit=1
        ).id

    name = fields.Char(string="Prospect Name", required=True, index=True,track_visibility='onchange')
    contact_name = fields.Char(string="Contact Name")

    website = fields.Char('Website', index=True, help="Website of the contact")
    itype = fields.Selection(selection=[('Walk In', 'Walk In'),
                             ('Site Visit', 'Site Visit'),
                             ('Open Day', 'Open Day'),
                             ('Investment Roadshow', 'Investment Roadshow'),
                             ('Call In', 'Call In'),
                             ('Call Out', 'Call Out'),
                             ('Email In', 'Email In'),
                             ('Email Out', 'Email Out'),
    ])

    cert = fields.Char('CERT')
    tin = fields.Char('TIN')
    type_invest = fields.Many2one('investment.types',string='Investment Types')
    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary("Image", attachment=True,
        help="This field holds the image used as avatar for this contact, limited to 1024x1024px",)
    image_medium = fields.Binary("Medium-sized image", attachment=True,
        help="Medium-sized image of this contact. It is automatically "\
             "resized as a 128x128px image, with aspect ratio preserved. "\
             "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image", attachment=True,
        help="Small-sized image of this contact. It is automatically "\
             "resized as a 64x64px image, with aspect ratio preserved. "\
             "Use this field anywhere a small image is required.")

    project_description = fields.Text()

        # Trying to remove the chatter messages
    user_id = fields.Many2one('res.users', string='Relationship Manager', default=lambda self: self.env.user, required=True,track_visibility='onchange')

    team_id = fields.Many2one(
        'crm.team',
        string='Department Team', oldname='section_id',
        default=lambda self: self.env['crm.team'].sudo()._get_default_team_id(user_id=self.env.uid),
        help='When sending mails, the default email address is taken from the Department Team.'
    )

    res_users_ids = fields.Many2one('res.users', string="Res Users link")
    department_name = fields.Many2many('res.users', relation="res_user_investor_link", column1='investor_ids', column2='res_users_ids', string="Team", track_visibility='onchange', store=True)
    # department_relation = fields.Char(related='department_name.res_user_investor_link.res_users_ids.ids', string='My Team Records')

    favorite_user_ids = fields.Many2many(
        'res.users', 'investor_team_favorite_user_rel', 'department_name', 'user_id',
        string='Favorite Members',
        default=_get_default_favorite_user_ids)
    is_favorite = fields.Boolean(
        string='Show on dashboard',
        compute='_compute_is_favorite', inverse='_inverse_is_favorite',
        help="Favorite teams to display them in the dashboard and access them easily.")
    start_date = fields.Date()
    investment_amount = fields.Integer()
    p_job_creation = fields.Char()
    p_address = fields.Char()
    sector = fields.Many2many('res.partner.industry', string='Sector',required=True,track_visibility='onchange',store=True)
    sector_view = fields.Char('Sector Tree View', related='sector.name', store=True)
    state = fields.Char(string='District')
    partner_id = fields.Many2many('res.partner', string='Prospect',  track_sequence=1, index=True,
        help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")
    active = fields.Boolean('Active', default=True)
    create_date = fields.Date('Create Date')
    describe = fields.Text(string="Prospect Description")

    planned_revenue = fields.Monetary('Expected Revenue', currency_field='company_currency')
    user_initials = fields.Char(string='User Initials',default=logged_user_initials)

    # File Uploads
    # document_upload = fields.Binary(string='Upload Document Here')
    document_upload = fields.Many2one('muk_dms.file',string='Upload Document Here')
    # document_extras = fields.Many2many('muk_dms.file', string='Prospect Documents')
    document_extras = fields.One2many(comodel_name='muk_dms.file', inverse_name='prospect_document', string='Prospect Documents')

    subsector = fields.Char(string='Sub-Sector')
    # x_sector = fields.Many2one(comodel_name='res.partner.industry', string='Sub Sectors')
    
    x_sub_sector = fields.Many2many('res.partner.sub_sector', string='Sub Sector')


    #link with projects

    project_id = fields.Many2one('project.project', string='Project Link', required=False)
    project_ids = fields.Many2many('project.project', relation='project_project_investors_link',
                                   column1='investor_id', column2='project_id', string='Project')
    project_count = fields.Integer('Project Count', compute='_compute_project_count', track_visibility='onchange')

    project_tag_ids = fields.Many2one('project.tags', string = 'Project Tags Link')
    investor_tags = fields.Many2many('project.tags', relation='investor_project_tags', column1='investor_ids', column2='project_tag_ids', string="Opportunity")

    res_users_ids = fields.Many2one('res.users', string="Res Users link")

    #link with company
    res_partner_id = fields.Many2one('res.partner', 'Company', required=False,default=None)
    x_company_count_ids = fields.Many2many('res.partner', relation='res_partner_crm_lead_links',
                                    column1='crm_lead_id', column2='res_partner_id', string='Company', domain="[('x_company_cat', '=', 'company')]")
    x_company_count = fields.Integer('Company Count', compute='_compute_company_count',track_visibility='onchange')

    #link with task
    task_count_ids = fields.One2many('project.task', 'lead_id', string="Opp Count")
    task_id = fields.Many2one('project.task', string='Task Link', required=False)
    task_ids = fields.Many2many('project.task', relation='crm_lead_task_link', column1='lead_id', column2='task_id', string='Task')
    task_count = fields.Integer('Tasks Count', compute='_compute_task_count',track_visibility='onchange')

    #link with request
    request_id = fields.Many2one('helpdesk.ticket', string='Request Link', required=False)
    request_ids = fields.Many2many('helpdesk.ticket', relation='helpdesk_investors_link', column1='investor_id', column2='request_id',string='Issue')
    request_count = fields.Integer('Requests Count', compute='_compute_request_count',track_visibility='onchange')

    stage_id = fields.Many2one('crm.stage', string='Stage', ondelete='restrict', index=True,
        domain="['|', ('team_id', '=', False), ('team_id', '=', team_id)]",track_visibility='always', group_expand='_read_group_stage_ids',store=True,default=lambda self: self._default_stage_id())
    stage_name = fields.Char(string="Current Prospect Stage", store=True,
                               related='stage_id.namefh_admission_tag_no
        help="Type is used to separate Leads and Opportunities")

    parent_id = fields.Many2one('res.partner', string='Name', index=True)
    investor_type = fields.Selection([('operator', 'Operator'),('financial','Financial')],string="Type", required=True, track_visibility='onchange')

    source = fields.Many2one('investor.source', string='Source', track_visibility='onchange')

    ref_type = fields.Many2one('investor.reftype', string="Referral Type",track_visibility='onchange')
    status = fields.Selection([('active','Active'),('inactive','Inactive')], default='active', string="Status",track_visibility='onchange')
    investor_event = fields.Text('Events')

    # contact_info = fields.Many2many('contact.person', string='Contacts')
    contact_info = fields.Many2many('res.partner', string='Contact Person', domain=[('active','=',True), ('type','=','other')], context="{'default_type':'other'}")
    # contact_info = fields.One2many('res.partner', 'project_id', string='Contacts',domain=[('active', '=', True), ('type', '=', 'contact')])

    child_id = fields.One2many('res.partner', 'parent_id', string='Contacts')
    country_id = fields.Many2one('res.country', string='Country', required=True)
    color = fields.Integer('Color Index', default=10)
    investor_tss = fields.Selection([('0', 'DA/Marketing'),('1', 'Strategic Deal'),
                                    ('2', 'Privatization'),
                                    ('3', 'PPP(Public Private Partnership)')], string='Type of Deal')

    _sql_constraints = [('name', 'unique(name)', 'A record with a similar name already exists! Name cannot be duplicate value for this field!')]

# ###################################################################
    def _compute_is_favorite(self):
        for team in self:
            team.is_favorite = self.env.user in team.favorite_user_ids

    view_visibility_field_referral = fields.Boolean(string='Referral Visible View', default=False)
    view_visibility_field_conference = fields.Boolean(string='Conference Visible View', default=False)

    @api.onchange('source')
    def on_change_source_referral(self):
        if self.source.is_referral == True:
            self.view_visibility_field_referral = True
        else:
            self.view_visibility_field_referral = False

    @api.onchange('source')
    def on_change_source_conference(self):
        if self.source.is_conference == True:
            self.view_visibility_field_conference = True
        else:
            self.view_visibility_field_conference = False

    def _rebuild_pls_frequency_table_threshold(self):
        """ Called by action_set_lost and action_set_won.
         Will run the cron to update the frequency table only if the number of lead is above
         a specified value (from config_parameter) for onboarding purpose.
         Once the threshold is reached, the config_param is set to 0 to avoid re-run the cron
         and, mainly, to avoid making useless search_count in the future."""
        pls_threshold = int(self.env['ir.config_parameter'].sudo().get_param('crm.pls_rebuild_threshold'))
        if pls_threshold:
            lead_count = self.env['crm.lead'].sudo().search_count([])
            if lead_count < pls_threshold:
                self.sudo()._cron_update_automated_probabilities()
            else:
                self.env['ir.config_parameter'].sudo().set_param('crm.pls_rebuild_threshold', 0)

    def action_set_lost(self, **additional_values):
        """ Lost semantic: probability = 0 or active = False """
        result = self.write({'active': False, 'status': 'passive', 'probability': 0, **additional_values})
        self._rebuild_pls_frequency_table_threshold()
        return result


    def reactivate_investor(self):
        self.write({'active': True, 'status': 'active'})

    def e164_convert(self, phone_code, mobile):
        if mobile:
            if phone_code:
                if mobile.startswith("0"):
                    return "+" + str(phone_code) + mobile[1:].replace(" ","")
                elif mobile.startswith("+"):
                    return mobile.replace(" ","")
                else:
                    return "+" + str(phone_code) + mobile.replace(" ","")
            else:
                return mobile.replace(" ", "")

    # @api.onchange('project_ids')
    # @api.depends('project_ids')
    # def _onchange_sector(self):
    #     if not len(self.sector) > 1:
    #         raise UserError('Sorry, you need to choose a sector first')
    # @api.depends('sector')
    # def first_sector(self):
    #     if 0 == len(self.sector):
    #         raise UserError("Please choose a Sector before you proceed")
    #     else:
    #         self.sector[0].id



#create lead
    # Allows user to create a project and move to the stage that needs a project.
    @api.onchange('stage_id','project_count', 'x_company_count', 'project_ids','source')
    @api.depends('stage_id','project_count', 'x_company_count', 'project_ids', 'source')
    def _onchange_stage_identity(self):
        project_stage = self.env['crm.stage'].search([('is_project','=',True)]).id
        company_stage = self.env['crm.stage'].search([('is_company','=',True)]).id
        inactive_stage = self.env['crm.stage'].search([('is_inactive','=',True)]).id
        static_stage = self.env['crm.stage'].search([('static_state','=',True)]).id
        default_stage = self.env['crm.stage'].search([('default_stage','=',True)]).id

        if self.stage_id.is_project and self.project_count == 0:
            raise UserError('Cannot move Prospect '+str(self.name)+
                ' to this stage without a Project. Kindly Create/Add a Project for this Prospect in the Form View')

        if self.stage_id.is_company and self.x_company_count == 0:
            raise UserError('Cannot move Prospect '+str(self.name)+
                ' to this stage without a Company. Kindly Register/Add a Company for this Prospect in the Form View')


        # if (self.source == 'walkin' or 'referral') and self.stage_id.default_stage and self.x_company_count == 0 and self.project_count == 0:
        #     self.update({'stage_id': static_stage})

        if self.stage_id.is_project and self.project_count >= 1:
            # print("IS PROJECT!!!+++++++++")
            self.update({'stage_id':project_stage})

        if self.stage_id.is_company and self.x_company_count >= 1:
            # print("IS COMPANY!!!!++++++++++++")
            self.update({'stage_id': company_stage})

    @api.model
    def create(self, vals):
        project_stage = self.env['crm.stage'].search([('is_project','=',True)]).id
        company_stage = self.env['crm.stage'].search([('is_company', '=', True)]).id
        default_stage = self.env['crm.stage'].search([('default_stage', '=', True)]).id

        # if 'country_id' in vals and 'mobile' in vals:
        #     phone_code = self.env['res.country'].browse(int(vals['country_id'])).phone_code
        #     vals['mobile'] = self.e164_convert(phone_code, vals['mobile'])

        # if not vals.get('project_ids') and vals.get('x_company_count_ids'):
        #     print("Inside If default")

        #     vals.update({'stage_id': default_stage})

        if vals.get('project_ids') and len(vals['project_ids']) >= 2:
            # print("vals.get('project_ids')......______++++++++++")
            # print(vals.get('project_ids'))
            # print(len(vals['project_ids']))
            # print("Inside If Project")

            vals.update({'stage_id': project_stage})

        if vals.get('x_company_count_ids') and len(vals['x_company_count_ids']) >= 2:
            # print("vals.get('x_company_count_ids').....................----------------")
            # print(vals.get('x_company_count_ids'))
            # print(len(vals['x_company_count_ids']))
            # print("Inside If Company")
            vals.update({'stage_id': company_stage})

        if not vals.get('project_ids', False):
            try:
                project = self.env['project.project'].create(vals['project_ids'][0][2])
            except:
                raise ValidationError(_(
                        'The project cannot be saved without the Prospect. Kindly save the Prospect first and then add a project.'))
                # return vals['project_ids'].create()
            return project


        record = super(crm_lead, self).create(vals)
        #Add followers to record - Team Members and Relationship manager
        # for Adding document followers automatically.
        partner_list = []
        for items in record.department_name:
            # print("Debug: Loop users")
            # assuming login is set as email
            user_email = items.login
            partner = self.env['res.partner'].search([('email', '=', user_email)], limit=1)
            if partner:  # then add as a follower
                # append to list
                partner_list.append(partner.id)
        # we also and department head as a follower
        relationship_manager = self.get_department_head_from_relationship_manager(record.user_id)
        if relationship_manager:
            # append
            partner_list.append(relationship_manager)
        # subscribe
        record.message_subscribe(partner_list)

        return record
    #custom function to get relation manager
    # get department head to add as a follower
    def get_department_head_from_relationship_manager(self, user_id):
        # search request with user id in hr employee model
        employee_object = self.sudo().env['hr.employee'].search([('user_id', '=', user_id.id)], limit=1)
        # get head detail
        department_head_email = employee_object.department_id.manager_id.work_email
        # get relationship manager
        # pass the user to our function to get the related partner
        partner_object = self.env['res.partner'].search([('email', '=', department_head_email)], limit=1)
        # print('Partner to notify {} '.format(partner_object.id))
        return partner_object.id

    # A function that accepts users and returns related partners
    def get_partners_from_users(self, list_users):
        new_partner_list = []
        # loop items and do a search
        users = self.env['res.users'].search([('id', 'in', list_users)])
        for items in users:
            # print("Debug: Loop users")
            # assuming login is set as email
            user_email = items.login
            partner = self.env['res.partner'].search([('email', '=', user_email)], limit=1)
            if partner:  # then add as a follower
                # append to list
                new_partner_list.append(partner.id)
        return new_partner_list
    @api.multi
    def write(self, vals):
        project_stage = self.env['crm.stage'].search([('is_project','=',True)]).id
        company_stage = self.env['crm.stage'].search([('is_company','=',True)]).id
        # inactive_stage = self.env['crm.stage'].search([('is_inactive','=',True)]).id
        # static_stage = self.env['crm.stage'].search([('static_state','=',True)]).id
        # project_mode = self.env['project.project']
        # stage change: update date_last_stage_update

        if 'stage_id' in vals:
            vals['date_last_stage_update'] = fields.Datetime.now()

        if vals.get('project_ids') and len(vals['project_ids']) >= 1:
            vals.update({'stage_id':project_stage})

        if vals.get('x_company_count_ids') and len(vals['x_company_count_ids']) >= 1:
            vals.update({'stage_id':company_stage})

        # Only write the 'date_open' if no salesperson was assigned.
        if vals.get('user_id') and 'date_open' not in vals and not self.mapped('user_id'):
            vals['date_open'] = fields.Datetime.now()
        # stage change with new stage: update probability and date_closed
        if vals.get('stage_id') and 'probability' not in vals:
            vals.update(self._onchange_stage_id_values(vals.get('stage_id')))

        if vals.get('probability', 0) >= 100 or not vals.get('active', True):
            vals['date_closed'] = fields.Datetime.now()

        elif 'probability' in vals:
            vals['date_closed'] = False

        if 'country_id' in vals and 'mobile' in vals:
            phone_code = self.env['res.country'].browse(int(vals['country_id'])).phone_code
            vals['mobile'] = self.e164_convert(phone_code, vals['mobile'])
        if 'country_id' in vals and 'mobile' not in vals:
            phone_code = self.env['res.country'].browse(int(vals['country_id'])).phone_code
            vals['mobile'] = self.e164_convert(phone_code, self.mobile)
        if 'country_id' not in vals and 'mobile' in vals:
            vals['mobile'] = self.e164_convert(self.country_id.phone_code, vals['mobile'])
        ############### changing subscribers
        # get the variable for team from submitted variable
        new_users_to_add = vals.get('department_name') or None
        # not none
        if new_users_to_add:
            # current prospect
            prospect_object = self.env['crm.lead'].search([('id', '=', self.id)], limit=1)
            # get existing partners
            existing_users = prospect_object.department_name.ids
            existing_partners = self.get_partners_from_users(existing_users)
            # remove current followers
            prospect_object.message_unsubscribe(existing_partners)
            # now get the current subscribers
            partners = self.get_partners_from_users(new_users_to_add[0][2])
            #add subscription
            prospect_object.message_subscribe(partners)
            #########
        # Cater for Request to only allow users who are either prospect lead / or in prospect team to edit a prospect
        # so check current user editing the prospect is in the list of team or is the prospect lead
        lead_user = self.user_id.id
        team_users = [i for i in self.department_name.ids]
        # add lead to team
        team_users.append(lead_user)
        # now check if user creating is in the list / Also admins can override this and project lead
        # or self.env.user.has_group('base.group_erp_manager')
        if self.env.uid in team_users or self.env.uid == 1:
            # is the lead transfering this record ?
            if vals.get('user_id'):
                # one can only change lead if he/she is the lead in the current Prospect
                if self.env.uid != lead_user:
                    raise ValidationError(_(
                        'Warning! Sorry,cannot change Relationship Manager. You can only change this if you are the Relationship Manager'))
            # write data and return
            return super(crm_lead, self).write(vals)
        else:
            raise ValidationError(_(
                'Warning! Sorry,cannot save the new changes. Only Prospect Team members / Relationship Manager who can edit this record.'))


    @api.multi
    def create_projects_view(self):
        project_stage = self.env['crm.stage'].search([('is_project','=',True)]).id
        stage = self.env['project.task.type'].sudo().search([('name', '!=', 'None')])

        # if self.project
        self.update({'stage_id':project_stage})

        print(self.describe, "%%%%%%%%%%%")
        return {

            'type': 'ir.actions.act_window',
            # 'flags': {'form': {'action_buttons': True}},
            'name': 'Project Details',
            'res_model': 'project.project',
            'view_type': 'form',
            'view_mode': 'form',
            # 'view_id': self.env.ref('investor_contact.investor_project_edit_link', False).id,
            'view_id': self.env.ref('project.edit_project', False).id,
            'target': 'new',
            'context': {
                'default_name': self.name,
                # include description
                # 'default_describe':self.project_description,
                'default_investor_id': self.id,
                'default_investor_ids':[(4, self.id)],
                'default_investor_sector': None if 0 == len(self.sector) else self.sector[0].id,
                'default_x_state': 'prospective',
                'default_stage_id': stage[0].id,
            },
        }

    @api.multi
    def create_company_view(self):
        company_stage = self.env['crm.stage'].search([('is_company','=',True)]).id

        self.update({'stage_id': company_stage})

        return {
            'type': 'ir.actions.act_window',
            'name': 'Create a Company',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            # 'view_id': self.env.ref('res_partner_addons.res_partner_sales_replacement_form').id,
            'view_id': self.env.ref('investor_contact.res_partner_investor_form', False).id,
            'context': {
                'default_is_company': True,
                'default_company_type': 'company',
                'default_x_company_cat': 'company',
                'default_crm_lead_id':self.id,
                'default_x_investor_count_ids':[(4, self.id)],
                'default_modal_view': True,
                'default_x_registered_project': self.id,
                'default_name': self.name,
                'default_x_sector': None if 0 == len(self.sector) else self.sector[0].id,
                 # [(4, tag.id) for tag in self.tag_projects_ids]
            },
            # self.update({'stage_id':company_stage})
        }

# ############################################################################

    # @api.multi
    # def qualified(self):
        # self.type = 'opportunity'

# ############################################################################

    # Sets the Title Name at the top of the breadcrumbs to desired value.

    # @api.multi
    # @api.depends('partner_name')
    # def name_get(self):
    #     res = []
    #     for record in self:
    #         res.append((record.id, "%s " % (record.partner_name.name)) or 'New')
    #     return res

# ############################################################################


# we need this to get the correct res.partner view
    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super(crm_lead, self).fields_get(allfields, attributes)
        node = self.env.ref('res_partner_addons.action_res_partner_company').read()[0]
        for key, row in res.items():
            if 'x_company_count_ids' == key:
                row['context'] = node['context']
        return res

    # # Adding Counters to Smart Buttons
    @api.depends('stage_id','x_company_count')
    @api.multi
    def _compute_company_count(self):
        for rec in self:
            rec.x_company_count = len(rec.x_company_count_ids)

    @api.multi
    def _compute_project_count(self):
        for rec in self:
            rec.project_count = len(rec.project_ids)

    @api.multi
    def _compute_task_count(self):
        for rec in self:
            rec.task_count = len(rec.task_ids)

    @api.multi
    def _compute_request_count(self):
        for rec in self:
            rec.request_count = len(rec.request_ids)

    @api.multi
    def action_schedule_meeting_custom(self):
        """ Open meeting's calendar view to schedule meeting on current opportunity.
            :return dict: dictionary value for created Meeting view
        """
        self.ensure_one()
        action = self.env.ref('calendar.action_calendar_event').read()[0]
        partner_ids = self.env.user.partner_id.ids
        if self.contact_info:
            for investor in self.contact_info:
                partner_ids.append(investor.id)
        action['context'] = {
            'default_opportunity_id': self.id if self.type == 'opportunity' else False,
            'default_partner_id': self.partner_id.id,
            'default_partner_ids': partner_ids,
            'default_team_id': self.team_id.id,
            'default_name': self.name,
        }
        return action
