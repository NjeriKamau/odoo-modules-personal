# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, HRMS Leave Cancellation
#    Copyright (C) 2018 Hilar AK All Rights Reserved
#    https://www.linkedin.com/in/hilar-ak/
#    <hilarak@gmail.com>
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

from odoo import models, fields, api
from odoo.http import request
#import datetime
from datetime import datetime



class CRMDashboard(models.Model):
    _name = 'crm.dashboard'
    _description = 'CRM Dashboard'

    _inherit = ['mail.alias.mixin', 'mail.thread', 'mail.activity.mixin']  # ' 'mail.activity.mixin'

    name = fields.Char("")


    @api.multi
    def update_delayed_tasks(self):
        uid = request.session.uid
        cr = self.env.cr
        ##get delayed tasks
        query_tasks = """select pt.id,pty.name as stage from project_task pt 
                                             left join project_task_type pty on pt.stage_id = pty.id where pt.user_id = (%s) and pt.date_deadline < (%s) """
        user_ids_vars = uid
        cr.execute(query_tasks, [user_ids_vars,datetime.now().strftime('%Y-%m-%d')])
        tasks_table = cr.dictfetchall()
        #print (tasks_table)
        tasks_ids = [i['id'] for i in tasks_table]
        #print("Delayed tasks search ::::::::::::")

        #get task stage id set as is delayed stage
        task_delayed_type = self.env['project.task.type'].sudo().search([('is_delayed_task_stage', '=', True)],limit=1)
        task_delayed_type_res = [i.id for i in task_delayed_type]
        #print(task_delayed_type_res[0])
        #update all records to delayed
        #print(tasks_ids)
        #print(search_tasks)
        search_tasks = self.env['project.task'].sudo().browse(tasks_ids)

        update = search_tasks.sudo().write({'stage_id': task_delayed_type_res[0]})
    #Check user groups
    def check_access_to_investors(self):
        #check  if user has access to investors
        if (self.env.user.has_group('support_ticket_extend.irms_group_marketing')) or (self.env.user.has_group('support_ticket_extend.irms_group_deal_accelerator')):
            #print("Access Investors")
            return True

        else:
            return False
    #check user has access to projects
    def check_access_to_projects(self):
        #check  if user has access to investors
        if (self.env.user.has_group('support_ticket_extend.irms_group_deal_accelerator')):
            #print("Access Projects")
            return True

        else:
            return False
    #check user has access to companies
    def check_access_to_companies(self):
        #check  if user has access to investors
        if (self.env.user.has_group('support_ticket_extend.irms_group_aftercare')):
            #print("Access Companies")
            return True

        else:

            return False

    @api.model
    def get_crm_info(self):

        #house cleaning
        #1. - update tasks status on dashboard load
        self.update_delayed_tasks()

        #########################

        uid = request.session.uid
        cr = self.env.cr
        employee_id = self.env['hr.employee'].sudo().search_read([('user_id', '=', uid)], limit=1)
        query = """
                    select e.name as employee, j.name as job, d.name as department,
                    e.work_phone, e.work_email, e.work_location, e.gender, e.birthday, e.marital, e.passport_id from hr_employee e inner join hr_job j on (j.id = job_id)
                    inner join hr_department d on (e.department_id = d.id)

                """
        cr.execute(query)
        employee_table = cr.dictfetchall()

        #Get a list of my investors on the pipeline
        investors = self.env['crm.lead'].sudo().search([])
        total_investors = [i.name for i in investors]
        #print("Debug: get_crm_info() {0} >>>>>".format(total_investors))
        #get list of my tasks - All of them regardless of status
        tasks = self.env['project.task'].sudo().search([('user_id', '=', uid)])
        total_tasks = [i.name for i in tasks]
        # get list of my projects - Projects assigned to me
        projects = self.env['project.project'].sudo().search([('user_id', '=', uid)])
        total_projects = [i.name for i in projects]
        #my requests - Requests Assigned to me
        requests = self.env['website.support.ticket'].sudo().search([('user_id', '=', uid)])
        total_requests = [i.ticket_number for i in requests]
        #Get list of Tasks pending
        #get project stages marked as pending
        task_pending_type = self.env['project.task.type'].sudo().search([('is_pending_task_stage', '=', True)])
        task_pending_type_res = [i.id for i in task_pending_type]

        #tasks pending on time
        #print("Date time is ::::::::::::::::::::::::: {0}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        tasks_pending = self.env['project.task'].sudo().search([('user_id', '=', uid),
                                                                ('stage_id','=',task_pending_type_res[0])])
        total_tasks_pending = [i.name for i in tasks_pending]
        total_tasks_pending_check = 0
        #print("Tasks Length::::::::::::::::: {0}".format(len(total_tasks_pending)))
        if len(total_tasks_pending) > 0:
            total_tasks_pending_check = total_tasks_pending[0]
        #Investors my investors list
        # Get a list of my investors on the pipeline
        my_investors = self.env['crm.lead'].sudo().search([('user_id', '=', uid)])
        my_total_investors = [i.name for i in my_investors]

        #Get unattend type of stage
        unattended_type_stage = self.env['website.support.ticket.states'].sudo().search([('unattended', '=', True)])
        unattended_type_stage_res = [i.id for i in unattended_type_stage]
        #get list of my requests - Assigned to me and pending
        requests_pending = self.env['website.support.ticket'].sudo().search([('user_id', '=', uid),
                                                                             ('state', '=', unattended_type_stage_res[0])])
        total_requests_pending = [i.ticket_number for i in requests_pending]
        #companies
        companies = self.env['res.partner'].sudo().search([('is_company', '=', True),
                                                           ('x_ipa_staff','=',uid)])
        total_companies = [i.name for i in companies]
        #projects
        projects = self.env['project.project'].sudo().search([
                                                           ('user_id', '=', uid)])
        total_projects = [i.name for i in projects]
        #my files
        my_files = self.env['muk_dms.file'].sudo().search([
            ('create_uid', '=', uid)])
        total_my_files = [i.name for i in my_files]
        #my inbox
        # my files
        my_inbox = self.env['mail.channel'].sudo().search([
            ('create_uid', '=', uid)])
        total_my_inbox = [i.name for i in my_inbox]

        ##Chart for tasks
        query_tasks = """select pty.stage_chart_color as stage_color, count(pt.name) as no_of_tasks,pty.name as stage from project_task pt 
                                      left join project_task_type pty on pt.stage_id = pty.id where pt.user_id = (%s) and pty.is_done_task_stage != (%s) group by stage,stage_color """
        user_ids_vars = uid
        cr.execute(query_tasks,[user_ids_vars,True])
        tasks_table = cr.dictfetchall()
        tasks_labels = []
        tasks_dataset = []
        task_stage_colors = []
        #print("Before Loop ::::::::::::::::::;")
        for data in tasks_table:
            #print("There is data :::::::::::::::::")
            #print(data['stage'])
            tasks_labels.append(data['stage'])
            tasks_dataset.append(data['no_of_tasks'])
            task_stage_colors.append((data['stage_color']))
        ########################
        #Chart for Investors
        query_investors = """select count(i.name) as no_of_investors, s.name as stage from crm_lead  i
                             left join crm_stage s on s.id = i.stage_id where i.user_id = (%s) group by stage """

        cr.execute(query_investors, [user_ids_vars])
        investors_table = cr.dictfetchall()
        investors_labels = []
        investors_dataset = []
        for data in investors_table:
            investors_labels.append(data['stage'])
            investors_dataset.append(data['no_of_investors'])
        #Chart for Companies
        query_companies = """select count(r.name) as no_of_companies, s.name as stage from res_partner  r
                                     left join res_partner_stages s on s.id = r.x_invest_states 
                                     left join res_partner_ipa_staff_links pl on pl.res_partner_id = r.id
                                     where pl.res_users_id = (%s) and r.is_company = (%s) group by stage """

        cr.execute(query_companies, [user_ids_vars,True])
        companies_table = cr.dictfetchall()
        companies_labels = []
        companies_dataset = []
        for data in companies_table:
            companies_labels.append(data['stage'])
            companies_dataset.append(data['no_of_companies'])

        # Chart for projects
        query_projects = """select count(p.id) as no_of_projects, s.name as stage from project_project  p
                                     left join project_task_type s on s.id = p.stage_id 
                                     where p.user_id = (%s)  and s.is_task_stage = (%s) group by stage"""

        cr.execute(query_projects, [user_ids_vars, False])
        projects_table = cr.dictfetchall()
        projects_labels = []
        projects_dataset = []
        #print("Before loop ::::::")
        for data in projects_table:
            #print ("In loop:::::")
            #print(data['no_of_projects'])
            #print(data['stage'])
            projects_labels.append(data['stage'])
            projects_dataset.append(data['no_of_projects'])



        #Chart for Requests
        """query_requests = select st.state_color as stage_color, count(t.id) as no_of_tickets,st.name as stage from website_support_ticket t 
           left join website_support_ticket_states st on st.id = t.state
           where t.user_id = (%s) and st.is_done_state = (%s) group by stage,stage_color """
        ##
        query_requests = """ select count(t.id) as no_of_tickets,status as stage from website_support_ticket t 
                  where t.user_id = (%s) group by stage """
        user_ids_vars = uid
        cr.execute(query_requests, [user_ids_vars])
        tickets_table = cr.dictfetchall()
        tickets_labels = []
        tickets_dataset = []
        tickets_stage_colors = []
        for data in tickets_table:
            ##Do not show completed
            if data['stage'] != 'completed':

                tickets_dataset.append(data['no_of_tickets'])
                #TODO - fix this
                if data['stage'] == 'on_time':
                    tickets_labels.append('On Time')
                    color = "#00FF00"
                    tickets_stage_colors.append(color)
                elif data['stage'] == 'delayed':
                    color = "#FF0000"
                    tickets_labels.append('Delayed')
                    tickets_stage_colors.append(color)
                elif data['stage'] == 'systemic':
                    tickets_labels.append('Systemic')
                    color = "#0000FF"
                    tickets_stage_colors.append(color)
                else:
                    tickets_labels.append('Unknown')
                    color = "#000000"
                    tickets_stage_colors.append(color)
                ########################

        #print("Initial >>>>>>>>>>>>>>>>>> {0}".format(task_pending_type_res[0]))
        if employee_id:
            categories = self.env['hr.employee.category'].sudo().search([('id', 'in', employee_id[0]['category_ids'])])
            data = {
                'categories': [c.name for c in categories],
                'emp_table': employee_table,
                'total_investors': len(total_investors) ,
                'total_tasks': len(total_tasks),
                'total_projects': len(total_projects),
                'total_requests': len(requests),
                #Tasks stuff
                'task_stage_to_check': total_tasks_pending_check,
                'my_pending_tasks': len(total_tasks_pending),
                'my_user_id': uid,
                #investors stuff
                'my_total_investors': len(my_total_investors),
                #requests
                'my_pending_requests': len(total_requests_pending),
                'unattend_stage_id': unattended_type_stage_res[0],
                #companies
                'total_companies': len(total_companies),
                #my projects
                'total_projects': len(total_projects),
                #my files
                'total_my_files': len(total_my_files),
                #inbox
                'total_my_inbox': len(total_my_inbox),
                ########### chart for tasks
                'tasks_labels' : tasks_labels ,
                'tasks_dataset' : tasks_dataset,
                'task_stage_colors': task_stage_colors,
                'tickets_stage_colors': tickets_stage_colors,
                #stage for all tasks
                'initial_task_pending_stage': task_pending_type_res[0],
                ### chart for investors
                'investors_labels': investors_labels,
                'investors_dataset':investors_dataset,
                #####chart for companies
                'companies_labels': companies_labels,
                'companies_dataset': companies_dataset,
                #####chart for projects
                'projects_labels': projects_labels,
                'projects_dataset': projects_dataset,
                #### chart for tickets
                'tickets_labels': tickets_labels,
                'tickets_dataset': tickets_dataset,
                ###Groups checking
                'check_investors': self.check_access_to_investors(),
                'check_projects': self.check_access_to_projects(),
                'check_companies': self.check_access_to_companies()

            }
            employee_id[0].update(data)
        return employee_id
        #return True


    @api.model
    def get_employee_info(self):
        """
        The function which is called from hr_dashboard.js.
        To fetch enough data from model hr and related dependencies.
        :payroll_dataset Total payroll generated according to months from model hr_payslip and hr_payslip_lines.
        :attendance_data Total worked hours and attendance details from models hr_attendace and hr_employee.
        :employee_table dict of datas from models hr_employee, hr_job, hr_department.
        :rtype dict
        :return: data
        """
        uid = request.session.uid
        cr = self.env.cr
        employee_id = self.env['hr.employee'].sudo().search_read([('user_id', '=', uid)], limit=1)
        leave_search_view_id = self.env.ref('hr_holidays.view_hr_holidays_filter')
        timesheet_search_view_id = self.env.ref('hr_timesheet.hr_timesheet_line_search')
        job_search_view_id = self.env.ref('hr_recruitment.view_crm_case_jobs_filter')
        attendance_search_view_id = self.env.ref('hr_attendance.hr_attendance_view_filter')
        expense_search_view_id = self.env.ref('hr_expense.view_hr_expense_sheet_filter')
        leaves_to_approve = self.env['hr.holidays'].sudo().search_count([('state', 'in', ['confirm', 'validate1']),
                                                                         ('type', '=', 'remove')])
        leaves_alloc_to_approve = self.env['hr.holidays'].sudo().search_count([('state', 'in', ['confirm', 'validate1'])
                                                                                  ,('type', '=', 'add')])
        timesheets = self.env['account.analytic.line'].sudo().search_count(
            [('project_id', '!=', False), ])
        timesheets_self = self.env['account.analytic.line'].sudo().search_count(
            [('project_id', '!=', False), ('user_id', '=', uid)])
        job_applications = self.env['hr.applicant'].sudo().search_count([])
        attendance_today = self.env['hr.attendance'].sudo().search_count([('check_in', '>=',
                            str(datetime.datetime.now().replace(hour=0, minute=0, second=0))),
                            ('check_in', '<=', str(datetime.datetime.now().replace(hour=23, minute=59, second=59)))])
        expenses_to_approve = self.env['hr.expense.sheet'].sudo().search_count([('state', 'in', ['submit'])])

        # payroll Datas for Bar chart
        query = """
            select to_char(to_timestamp (date_part('month', p.date_from)::text, 'MM'), 'Month') as Month, sum(pl.amount)
            as Total from hr_payslip p
            INNER JOIN hr_payslip_line pl
                on (p.id = pl.slip_id and pl.code = 'NET' and p.state = 'done')
            group by month, p.date_from order by p.date_from
        """
        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        for data in payroll_data:
            payroll_label.append(data['month'])
            payroll_dataset.append(data['total'])

        # Attendance Chart Pie
        query = """
            select sum(a.worked_hours) as worked_hours, e.name as employee
            from hr_attendance a
            inner join hr_employee e on(a.employee_id = e.id)
            group by e.name
        """
        cr.execute(query)
        attendance_data = cr.dictfetchall()
        attendance_labels = []
        attendance_dataset = []
        for data in attendance_data:
            attendance_labels.append(data['employee'])
            attendance_dataset.append(data['worked_hours'])

        query = """
            select e.name as employee, e.barcode as badge_id, j.name as job, d.name as department,
            e.work_phone, e.work_email, e.work_location, e.gender, e.birthday, e.marital, e.passport_id,
            e.medic_exam, e.public_info from hr_employee e inner join hr_job j on (j.id = job_id)
            inner join hr_department d on (e.department_id = d.id)

        """
        cr.execute(query)
        employee_table = cr.dictfetchall()

        if employee_id:
            categories = self.env['hr.employee.category'].sudo().search([('id', 'in', employee_id[0]['category_ids'])])
            data = {
                'categories': [c.name for c in categories],
                'leave_search_view_id': leave_search_view_id.id,
                'timesheet_search_view_id': timesheet_search_view_id.id,
                'job_search_view_id': job_search_view_id.id,
                'attendance_search_view_id': attendance_search_view_id.id,
                'expense_search_view_id': expense_search_view_id.id,
                'leaves_to_approve': leaves_to_approve,
                'leaves_alloc_to_approve': leaves_alloc_to_approve,
                'timesheets': timesheets,
                'timesheets_user': timesheets_self,
                'expenses_to_approve': expenses_to_approve,
                'job_applications': job_applications,
                'attendance_today': attendance_today,
                'payroll_label': payroll_label,
                'payroll_dataset': payroll_dataset,
                'attendance_labels': attendance_labels,
                'attendance_dataset': attendance_dataset,
                'emp_table': employee_table,
            }
            employee_id[0].update(data)
        return employee_id
