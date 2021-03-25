from odoo import models, api, _, fields
from odoo import SUPERUSER_ID
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
import datetime
from datetime import timedelta
from datetime import datetime
from odoo.http import request
from odoo.exceptions import UserError, ValidationError,AccessError
from dateutil import relativedelta



class CrmLeadExtend(models.Model):
    _name = 'mail.activity'
    _inherit = 'mail.activity'

    investor_res_id = fields.Many2one('crm.lead', string="Prospect Record")
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Important'),
        ('2', 'Very Important'),
        ('3', 'Urgent'),
    ], default='0', index=True, string="Priority")
    summary = fields.Char('Summary', required="True")

    # @api.depends('res_model', 'res_id')
    # def _compute_res_name(self):
    #     for activity in self:
    #         if activity.res_id == 0:
    #             new_res_id = self.env['mail.activity'].sudo().search([('res_id', 'in', self.ids)])


    #         else:
    #             activity.res_name = self.env[activity.res_model].browse(activity.res_id).name_get()[0][1]
    #             # activity.res_name = "Prospect Task"



    #we customize this
    def get_new_user_messages(self):
        messages = self.env['mail.message'].search([['needaction', '=', True]],limit=20).message_format()
        return messages

    # def _get_needaction(self):
        """ Need action on a mail.message = notified on my channel """
        my_messages = self.env['mail.notification'].sudo().search([
            ('mail_message_id', 'in', self.ids),
            ('res_partner_id', '=', self.env.user.partner_id.id),
            ('is_read', '=', False)]).mapped('mail_message_id')
        for message in self:
            message.needaction = message in my_messages

    #get logged user
    def get_my_allowed_sectors(self):
        sectors = self.env['res.users'].search([('id','=',self.env.uid)])
        sectors_list = []
        for item in sectors:
            sectors_list.append(item.x_sector_ids.ids)
        return sectors_list

    # def count_rec_in_stage(self, stage_id):
    #     my_stages = self.env['crm.stage'].search([])
    #     list_ids = []
    #     for item in my_stages:
    #         list_ids.append(item.id)
    #     crm_stage = self.env['crm.lead'].search_count([('stage_id','==',list_ids)])

    #     return crm_stage
        # # show records associated with that stage
        # for rec in self:
        #     rec_count = rec.search_count([('stage_id','==',stage_id)])

    @api.model
    def retrieve_dashboard(self):
        #domain to filter dashboard as per logged in user
        domain = [('user_id', '=', self.env.uid ),('active','=',True)]
        group_fields = ['priority', 'create_date', 'stage_id', 'close_hours']
        # TODO: remove SLA calculations if user_uses_sla is false.
        user_uses_sla = self.user_has_groups('helpdesk.group_use_sla') and \
                        bool(self.env['helpdesk.team'].search(
                            [('use_sla', '=', True), '|', ('member_ids', 'in', self._uid), ('member_ids', '=', False)]))
        if user_uses_sla:
            group_fields.insert(1, 'sla_fail')
        HelpdeskTicket = self.env['helpdesk.ticket']
        tickets = HelpdeskTicket.read_group(domain + [('stage_id.is_close', '=', False)], group_fields, group_fields,
                                            lazy=False)
        team = self.env['helpdesk.team'].search([], limit=1, order='id asc')
        result = {
            'helpdesk_target_closed': self.env.user.helpdesk_target_closed,
            'helpdesk_target_rating': self.env.user.helpdesk_target_rating,
            'helpdesk_target_success': self.env.user.helpdesk_target_success,
            'today': {'count': 0, 'rating': 0, 'success': 0},
            '7days': {'count': 0, 'rating': 0, 'success': 0},
            'my_all': {'count': 0, 'hours': 0, 'failed': 0},
            'yellow_flag_count': {'count': 0},
            'my_high': {'count': 0, 'hours': 0, 'failed': 0},
            'my_urgent': {'count': 0, 'hours': 0, 'failed': 0},
            'show_demo': not bool(HelpdeskTicket.search([], limit=1)),
            'rating_enable': False,
            'success_rate_enable': user_uses_sla,
            'alias_name': team.alias_name,
            'alias_domain': team.alias_domain,
            'use_alias': team.use_alias,
        }

        def add_to(ticket, key="my_all"):
            result[key]['count'] += ticket['__count']
            result[key]['hours'] += ticket['close_hours']
            if ticket.get('sla_fail'):
                result[key]['failed'] += ticket['__count']

        for ticket in tickets:
            add_to(ticket, 'my_all')
            if ticket['priority'] == '2':
                add_to(ticket, 'my_high')
            if ticket['priority'] == '3':
                add_to(ticket, 'my_urgent')

        dt = fields.Date.today()
        tickets = HelpdeskTicket.read_group(domain + [('stage_id.is_close', '=', True), ('close_date', '>=', dt)],
                                            group_fields, group_fields, lazy=False)
        for ticket in tickets:
            result['today']['count'] += ticket['__count']
            if not ticket.get('sla_fail'):
                result['today']['success'] += ticket['__count']

        dt = fields.Datetime.to_string((datetime.today() - relativedelta.relativedelta(days=6)))
        tickets = HelpdeskTicket.read_group(domain + [('stage_id.is_close', '=', True), ('close_date', '>=', dt)],
                                            group_fields, group_fields, lazy=False)
        for ticket in tickets:
            result['7days']['count'] += ticket['__count']
            if not ticket.get('sla_fail'):
                result['7days']['success'] += ticket['__count']
        # Tickets for yellow flag - Low priority which is 1 OTB patch
        yellow_flag_tickets = HelpdeskTicket.read_group(domain + [('yellow_flag', '=', True)],
                                                        group_fields, group_fields, lazy=False)
        for t in yellow_flag_tickets:
            result['yellow_flag_count']['count'] += t['__count']
        # Push activities
        # result['user_activities'] = self.activity_user_count()

        # browse tasks
        task_stages = self.env['project.task.type'].search(
            [('is_done_task_stage', '=', True), ('is_task_stage', '=', True)])
        browse_tasks = self.env['project.task'].search([('user_id', '=', self._uid),
                                                        ('helpdesk_id', '!=', False),
                                                        ('stage_id', '!=', task_stages.ids[0])], limit=2)
        # browse user unread messages
        # self.get_new_user_messages()
        user_messages_list = []
        for item in self.get_new_user_messages():
            data = {
                'message': item.get('mail_message_id'),
                'from': item.get('res_partner_id'),
                'id': item.get('id'),
                'res_id': item.get('res_id'),
                'model': item.get('model'),
                'subject': item.get('subject'),
                'record_name': item.get('record_name'),
                'author_name': item.get('author_id.name'),
                'author_id': item.get('author_id.id'),
                'message_type': item.get('message_type'),
            }
            user_messages_list.append(data)

        result['user_messages_list'] = user_messages_list
        # count projects with my issues
        my_issues = self.env['helpdesk.ticket'].search([('user_id', '=', self.env.uid), ('project_ids', '!=', None)])
        my_issues_list_projects = []
        for sm in my_issues:
            my_issues_list_projects.append(sm.id)
        result['my_issues'] = len(my_issues)
        # delayed issues
        my_issues_delayed = self.env['helpdesk.ticket'].search([('user_id', '=', self.env.uid),
                                                                ('days_to_target', '<', 0),
                                                                ('complete', '=', False)])
        my_issues_delayed_list = []
        for sm in my_issues_delayed:
            my_issues_delayed_list.append(sm.id)
        result['my_issues_delayed'] = len(my_issues)


# Njeri Trial... Investors.

        name_list =self.env['crm.lead'].read_group(domain + [('active','=', True), ('stage_id.is_inactive', '!=', True)],['stage_id'],['stage_id'])
        stage_count_investor=list(map(lambda d:d['stage_id_count'], name_list))
        total_investors = sum(stage_count_investor)
        result['investor_stage_count'] = stage_count_investor
        investor_stage_name = list(map(lambda d:d['stage_id'][1], name_list))
        result['total_investors'] = total_investors
        result['invest_stage_name'] = investor_stage_name

    # **************** Investor Fortnight Records *******************
        dt = fields.Datetime.to_string((datetime.today() - relativedelta.relativedelta(weeks=2)))
        dt_fortnight = self.env['crm.lead'].read_group(domain + [('write_date','>=', dt), ('active','=', True), ('stage_id.is_inactive', '!=', True)],['stage_id'],['stage_id'])
        fortnight_stage_count = list(map(lambda d:d['stage_id_count'], dt_fortnight))
        total_fortnight_count = sum(fortnight_stage_count)
        result['fortnight_stage_count'] = fortnight_stage_count
        result['total_fortnight_count'] = total_fortnight_count

    # ********** Projects Section of Dashboard ***************
        dt = fields.Datetime.to_string((datetime.today() - relativedelta.relativedelta(weeks=2)))
        project_dashboard_fields = ['stage_id', 'project_investment_amount', 'project_job_created']
        project_dashboard_groupby = ['stage_id']
        project_dashboard = self.env['project.project'].read_group(domain , project_dashboard_fields, project_dashboard_groupby)
        project_dashboard_fortnight_rec = self.env['project.project'].read_group(domain + [('write_date', '>=', dt)], project_dashboard_fields, project_dashboard_groupby)

        project_dashboard_stage_name = list(map(lambda d:d['stage_id'][1], project_dashboard))
        project_dashboard_count = list(map(lambda d:d['stage_id_count'], project_dashboard))
        project_dashboard_count_total = sum(project_dashboard_count)
        project_dashboard_amount = list(map(lambda d:d['project_investment_amount'], project_dashboard))
        project_dashboard_amount_list = [f'{int(amount):,}' for amount in project_dashboard_amount]

        project_dashboard_amount_total = sum(project_dashboard_amount)
        project_dashboard_amount_total_sum = f'{int(project_dashboard_amount_total):,}'
        project_dashboard_job = list(map(lambda d:d['project_job_created'], project_dashboard))
        project_dashboard_job_list = [f'{int(job):,}' for job in project_dashboard_job]
        project_dashboard_job_total = sum(project_dashboard_job)
        project_dashboard_job_total_sum = f'{int(project_dashboard_job_total):,}'
        project_dashboard_fortnight = list(map(lambda d:d['stage_id_count'], project_dashboard_fortnight_rec))
        project_dashboard_fortnight_total = sum(project_dashboard_fortnight)

        result['project_dashboard_stage_name'] = project_dashboard_stage_name
        result['project_dashboard_count'] = project_dashboard_count
        result['project_dashboard_amount'] = project_dashboard_amount_list
        result['project_dashboard_job'] = project_dashboard_job_list

        result['project_dashboard_amount_total'] = project_dashboard_amount_total_sum
        result['project_dashboard_count_total'] = project_dashboard_count_total
        result['project_dashboard_job_total'] = project_dashboard_job_total_sum
        result['project_dashboard_fortnight'] = project_dashboard_fortnight
        result['project_dashboard_fortnight_total'] = project_dashboard_fortnight_total

    # ********** Projects Quarterly Reports *********
        project_quarter_fields = ['project_investment_amount', 'project_job_created']
        project_dashboard_quarter_prospect = self.env['project.project'].read_group(domain+[('x_state', '=', 'prospective')], ['write_date'], ['write_date:quarter'] )
        project_dashboard_quarter_register = self.env['project.project'].read_group(domain+[('x_state', '=', 'registered')], project_quarter_fields + ['write_date'], ['write_date:quarter'] )

        dashboard_quarter_prospect_name = list(map(lambda d:d['write_date:quarter'], project_dashboard_quarter_prospect))
        dashboard_quarter_prospect = list(map(lambda d:d['write_date_count'], project_dashboard_quarter_prospect))
        dashboard_quarter_register = list(map(lambda d:d['write_date_count'], project_dashboard_quarter_register))
        dashboard_quarter_amount = list(map(lambda d:d['project_investment_amount'], project_dashboard_quarter_register))
        dashboard_quarter_jobs = list(map(lambda d:d['project_job_created'], project_dashboard_quarter_register))

        dashboard_quarter_amount_list = [f'{int(amount):,}' for amount in dashboard_quarter_amount]
        dashboard_quarter_jobs_list = [f'{int(job):,}' for job in dashboard_quarter_jobs]

        result['dashboard_quarter_prospect_name'] = dashboard_quarter_prospect_name
        result['dashboard_quarter_prospect'] = dashboard_quarter_prospect
        result['dashboard_quarter_register'] = dashboard_quarter_register
        result['dashboard_quarter_amount'] = dashboard_quarter_amount_list
        result['dashboard_quarter_jobs'] = dashboard_quarter_jobs_list

    # ************ Companies Reports ***************

        self.env.cr.execute('select count(distinct x_company_id) as cc from project_project where x_company_id is not NULL AND user_id = '+str(self.env.uid))
        company_dashboard_records = self.env.cr.dictfetchone()['cc']
        self.env.cr.execute("select count(id) as cc from res_partner where state = 're-invest' and x_ipa_user = "+str(self.env.uid))
        reinvest_dashboard_records = self.env.cr.dictfetchone()['cc']
        total_company_stats = company_dashboard_records + reinvest_dashboard_records

        result['company_dashboard_records'] = company_dashboard_records
        result['reinvest_dashboard_records'] = reinvest_dashboard_records
        result['total_company_stats'] = total_company_stats

        # counter of companies in the logged in user sectors
        sectors = self.get_my_allowed_sectors()
        list_sectors = []
        for items in sectors:
            list_sectors = items

        my_companies_list = self.env['res.partner'].search([('x_sector', 'in', list_sectors)])
        result['count_companies'] = len(my_companies_list)
        result['my_companies_list'] = my_companies_list
        # load tasks to display on dashboard of aftercare
        user_tasks_list = []
        for item in browse_tasks:
            due = item.date_deadline
            if due == False:
                due = 'Not Set'
            data = {
                'name': item.name,
                'issue': item.helpdesk_id.ticket_number,
                'status': item.stage_id.name,
                'deadline': due
            }
            user_tasks_list.append(data)
        result['user_tasks'] = user_tasks_list
        # listing activities
        list_activities = self.env['mail.activity'].search([('user_id', '=', self.env.uid)])
        # for i in list_activities:

        # activities_fields = ['deadline', 'summary', 'res_name', 'activity_type_id','user_id']
        # activities_fields_groupby= ['user_id']
        # activities_lists = self.env['mail.activity'].read_group(domain, activities_fields, activities_fields_groupby)

        my_activities_list = []
        # fields.Datetime.to_string((datetime.date.today() - relativedelta.relativedelta(days=14)))
        for item in list_activities:
            # fmt = '%Y-%m-%d'
            # dt = datetime.today()
            # deadline = datetime.strptime(item.date_deadline, fmt)

            # get the difference between todays date and deadline
            # The difference will determine what kind of error you get,
            # task_diff = fields.Datetime.to_string((datetime.date.today() - relativedelta.relativedelta(item.date_deadline)))
            # task_deadline = deadline - dt

            # task_deadline =  int(task_diff)
            # if task_deadline == timedelta(days=0):
            #     to_display = 'Today'
            # if task_deadline == timedelta(days=-1):
            #     to_display = 'Yesterday'
            # if task_deadline < timedelta(days=-1):
            #     to_display = '%d days overdue'%abs((task_deadline).days)
            # if task_deadline == timedelta(days=1):
            #     to_display = 'Tomorrow'
            # if task_deadline > timedelta(days=1):
            #     to_display = 'Due in %d days' % abs((task_deadline).days)


            details = item.summary
            if item.summary == '':
                details = item.note
            data = {
                'summary': details,
                'date_deadline': item.date_deadline,
                'res_model': item.res_model,
                'res_id': item.res_id,
                'res_name':item.res_name,
                'user_id':item.user_id.name,
                'user_id_id':item.user_id.id,
                'icon':item.icon,
                'state':item.state,
                'activity_type_id':item.activity_type_id.name,
                'activity_type_id_id':item.activity_type_id,
                'create_date':item.create_date,
                'date_deadline':item.date_deadline,
                'note':item.note,
                # 'label_delay':to_display,
                'id':item.id,
            }
            my_activities_list.append(data)

        result['my_activities_list'] = my_activities_list
        # get the time difference for display

        ##end
        result['today']['success'] = (result['today']['success'] * 100) / (result['today']['count'] or 1)
        result['7days']['success'] = (result['7days']['success'] * 100) / (result['7days']['count'] or 1)
        result['my_all']['hours'] = round(result['my_all']['hours'] / (result['my_all']['count'] or 1), 2)
        result['my_high']['hours'] = round(result['my_high']['hours'] / (result['my_high']['count'] or 1), 2)
        result['my_urgent']['hours'] = round(result['my_urgent']['hours'] / (result['my_urgent']['count'] or 1), 2)

        if self.env['helpdesk.team'].search(
                [('use_rating', '=', True), '|', ('member_ids', 'in', self._uid), ('member_ids', '=', False)]):
            result['rating_enable'] = True
            # rating of today
            domain = [('user_id', '=', self.env.uid)]
            dt = fields.Date.today()
            tickets = self.env['helpdesk.ticket'].search(
                domain + [('stage_id.is_close', '=', True), ('close_date', '>=', dt)])
            activity = tickets.rating_get_grades()
            total_rating = self.compute_activity_avg(activity)
            total_activity_values = sum(activity.values())
            team_satisfaction = round((total_rating / total_activity_values if total_activity_values else 0), 2)
            if team_satisfaction:
                result['today']['rating'] = team_satisfaction

            # rating of last 7 days (6 days + today)
            dt = fields.Datetime.to_string((datetime.date.today() - relativedelta.relativedelta(days=6)))
            tickets = self.env['helpdesk.ticket'].search(
                domain + [('stage_id.is_close', '=', True), ('close_date', '>=', dt)])
            activity = tickets.rating_get_grades()
            total_rating = self.compute_activity_avg(activity)
            total_activity_values = sum(activity.values())
            team_satisfaction_7days = round((total_rating / total_activity_values if total_activity_values else 0), 2)
            if team_satisfaction_7days:
                result['7days']['rating'] = team_satisfaction_7days
        return result
