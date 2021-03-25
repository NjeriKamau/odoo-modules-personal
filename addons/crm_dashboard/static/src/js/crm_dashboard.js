odoo.define('crm_dashboard.dashboard', function (require) {
"use strict";

var core = require('web.core');
var session = require('web.session');
var ajax = require('web.ajax');
var ActionManager = require('web.ActionManager');
var view_registry = require('web.view_registry');
var Widget = require('web.Widget');
var ControlPanelMixin = require('web.ControlPanelMixin');

var QWeb = core.qweb;

var _t = core._t;
var _lt = core._lt;

var CRMDashboardView = Widget.extend(ControlPanelMixin, {
//	template: 'hr_dashboard.dashboard',
	events: _.extend({}, Widget.prototype.events, {
		'click .leaves-left': 'leaves_left',
        'click .payslip': 'action_payslip',
        'click .timesheet': 'action_timesheet_user',
        'click .contract': 'action_contract',
        'click .leaves_to_approve': 'action_leaves_to_approve',
        'click .timesheets_to_approve': 'action_timesheets',
        'click .job_applications': 'action_job_applications',
        'click .leave_allocations': 'action_leave_allocations',
        'click .attendance': 'action_attendance',
        'click .expenses': 'action_expenses',
        'click #generate_payroll_pdf': function(){this.generate_payroll_pdf("bar");},
        'click #generate_attendance_pdf': function(){this.generate_payroll_pdf("pie")},
        'click .my_profile': 'action_my_profile',
        //Add custom actions
        'click .my_pending_tasks': 'action_my_pending_tasks',
        'click .my_investors': 'action_my_investors',
        'click .pending_requests': 'action_pending_requests',
        'click .companies': 'action_companies',
        'click .total_projects': 'action_total_projects',
        'click .total_my_files': 'action_total_files',
        'click .total_my_inbox': 'action_my_messaging',
	}),
	init: function(parent, context) {
        this._super(parent, context);
        var employee_data = [];
        var self = this;
        /*if (context.tag == 'crm_dashboard.dashboard') {
            self._rpc({
                model: 'crm.dashboard',
                method: 'get_employee_info',
            }, []).then(function(result){
                self.employee_data = result[0]
            }).done(function(){
                self.render();
                self.href = window.location.href;
            });
        }*/
          if (context.tag == 'crm_dashboard.dashboard') {
            self._rpc({
                model: 'crm.dashboard',
                method: 'get_crm_info',
            }, []).then(function(result){
                self.employee_data = result[0]

            }).done(function(result){
                self.render();

                   //Simple hide divs
                if (self.employee_data.check_investors == false){
                  //console.log("Hide investors >>>>> ") ;
                  //
                  var x = document.getElementById("my_investors_div");
                  x.style.display = "none";

                  var x2 = document.getElementById("total_investors_div");
                   x2.style.display = "none";

                }
                if (self.employee_data.check_projects == false){
                  //console.log("Hide projects >>>>> ") ;
                   var x = document.getElementById("my_projects_div");
                   x.style.display = "none";

                   var x2 = document.getElementById("total_projects_div");
                   x2.style.display = "none";
                }
                if (self.employee_data.check_companies == false){
                  //console.log("Hide companies >>>>> ") ;
                  var x = document.getElementById("my_companies_div");
                   x.style.display = "none";
                }
                self.href = window.location.href;
            });
        }
    },
    willStart: function() {
         return $.when(ajax.loadLibs(this), this._super());
    },
    start: function() {
        var self = this;
        return this._super();
    },
    render: function() {
        var super_render = this._super;
        var self = this;
        var crm_dashboard = QWeb.render( 'crm_dashboard.dashboard', {
            widget: self,
        });
        $( ".o_control_panel" ).addClass( "o_hidden" );
        $(crm_dashboard).prependTo(self.$el); //o_main_content o_content
         //console.log(self.$el);
         self.graph();
         //Check user group


        return crm_dashboard
    },
    reload: function () {
            window.location.href = this.href;
    },
    //Get total pending tasks
    action_my_pending_tasks: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("My Pending Tasks"),
            type: 'ir.actions.act_window',
            res_model: 'project.task',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    //'search_default_employee_id': [self.employee_data.id],
                    'default_stage_id': self.employee_data.initial_task_pending_stage,
                    },
            domain: [
                     ['user_id','=',self.employee_data.my_user_id]
            ],

            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})

    } ,

    //Get total Investors
    action_my_investors: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("My Investors"),
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'kanban'],[false, 'list'],[false, 'form']],
            context: {
                    //'search_default_employee_id': [self.employee_data.id],
                    //'default_employee_id': self.employee_data.id,
                    },
            domain: [['user_id','=',self.employee_data.my_user_id]
            ],

            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})

    } ,

        //Get total action_pending_requests
    action_pending_requests: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("My Requests"),
            type: 'ir.actions.act_window',
            res_model: 'website.support.ticket',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    //'search_default_employee_id': [self.employee_data.id],
                    //'default_employee_id': self.employee_data.id,
                    },
            domain: [['user_id','=',self.employee_data.my_user_id],
                    ['state','=',self.employee_data.unattend_stage_id]
            ],

            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})

    } ,
    //action_companies
    action_companies: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Companies"),
            type: 'ir.actions.act_window',
            res_model: 'res.partner',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    //'search_default_employee_id': [self.employee_data.id],
                    //'default_employee_id': self.employee_data.id,
                    },
            domain: [['x_ipa_staff','=',self.employee_data.my_user_id]
            ],

            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})

    } ,
    //action_total_projects
     action_total_projects: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Projects"),
            type: 'ir.actions.act_window',
            res_model: 'project.project',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    //'search_default_employee_id': [self.employee_data.id],
                    //'default_employee_id': self.employee_data.id,
                    },
            domain: [['user_id','=',self.employee_data.my_user_id]
            ],

            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})

    } ,
     //action_total_files
     action_total_files: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Companies"),
            type: 'ir.actions.act_window',
            res_model: 'muk_dms.file',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    //'search_default_employee_id': [self.employee_data.id],
                    //'default_employee_id': self.employee_data.id,
                    },
            domain: [['create_uid','=',self.employee_data.my_user_id]
            ],

            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})

    } ,
    //action_my_messaging
     action_my_messaging: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("My Inbox"),
            type: 'ir.actions.act_client',
            res_model: 'mail.channel',
            //view_mode: 'tree,form',
            //view_type: 'form',
            //views: [[false, 'list'],[false, 'form']],
            context: {
                    //'search_default_employee_id': [self.employee_data.id],
                    //'default_employee_id': self.employee_data.id,
                    },
            domain: [['create_uid','=',self.employee_data.my_user_id]
            ],

            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})

    } ,
    //
    leaves_left: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        return this.do_action({
            name: _t("Leaves"),
            type: 'ir.actions.act_window',
            res_model: 'hr.holidays',
            src_model: 'hr.employee',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {'search_default_employee_id': [self.employee_data.id],
                    'default_employee_id': self.employee_data.id,
                    'search_default_group_type': true,
                    'search_default_year': true
                    },
            domain: [['holiday_type','=','employee'], ['holiday_status_id.limit', '=', false], ['state','!=', 'refuse']],
            search_view_id: self.employee_data.leave_search_view_id,
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },
    action_payslip: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Payslips"),
            type: 'ir.actions.act_window',
            res_model: 'hr.payslip',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'search_default_employee_id': [self.employee_data.id],
                    'default_employee_id': self.employee_data.id,
                    },
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },
    action_timesheet_user: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Timesheets"),
            type: 'ir.actions.act_window',
            res_model: 'account.analytic.line',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'search_default_employee_id': [self.employee_data.id],
                    'search_default_month': true,
                    },
            domain: [['project_id', '!=', false]],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },
    action_contract: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Contracts"),
            type: 'ir.actions.act_window',
            res_model: 'hr.contract',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'kanban'],[false, 'list']],
            context: {
                    'search_default_employee_id': [self.employee_data.id],
                    'default_employee_id': self.employee_data.id,
                    },
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },
    action_leaves_to_approve: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Department Leaves"),
            type: 'ir.actions.act_window',
            res_model: 'hr.holidays',
            view_mode: 'tree,form,calendar',
            view_type: 'form',
            views: [[false, 'list'],[false, 'calendar']],
            context: {
                    'search_default_approve': true,
                    },
            domain: [['type','=','remove'],],
            search_view_id: self.employee_data.leave_search_view_id,
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },
    action_timesheets: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("All Timesheets"),
            type: 'ir.actions.act_window',
            res_model: 'account.analytic.line',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'search_default_week': true,
                    'search_default_groupby_employee': true,
                    'search_default_groupby_project': true,
                    'search_default_groupby_task': true,
                    },
            domain: [['project_id', '!=', false]],
            search_view_id: self.employee_data.timesheet_search_view_id,
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },
    action_job_applications: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Applications"),
            type: 'ir.actions.act_window',
            res_model: 'hr.applicant',
            view_mode: 'kanban,tree,form,pivot,graph,calendar',
            view_type: 'form',
            views: [[false, 'kanban'],[false, 'list'],[false, 'form'],
                    [false, 'pivot'],[false, 'graph'],[false, 'calendar']],
            context: {},
            search_view_id: self.employee_data.job_search_view_id,
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },
    action_leave_allocations: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Department Leaves Allocation"),
            type: 'ir.actions.act_window',
            res_model: 'hr.holidays',
            view_mode: 'tree,form,calendar',
            view_type: 'form',
            views: [[false, 'list'],[false, 'calender']],
            context: {
                    'search_default_approve': true,
                    },
            domain: [['type','=','add'],],
            search_view_id: self.employee_data.leave_search_view_id,
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },
    action_attendance: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Attendances"),
            type: 'ir.actions.act_window',
            res_model: 'hr.attendance',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'search_default_today': true,
                    },
            domain: [],
            search_view_id: self.employee_data.attendance_search_view_id,
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },
    action_expenses: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Expense Reports to Approve"),
            type: 'ir.actions.act_window',
            res_model: 'hr.expense.sheet',
            view_mode: 'tree,kanban,form,pivot,graph',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form'],[false, 'kanban'],[false, 'pivot'],[false, 'graph']],
            context: {
                    'search_default_submitted': true,
                    },
            domain: [],
            search_view_id: self.employee_data.attendance_search_view_id,
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },
    action_my_profile: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("My Profile"),
            type: 'ir.actions.act_window',
            res_model: 'hr.employee',
            res_id: self.employee_data.id,
            view_mode: 'form',
            view_type: 'form',
            views: [[false, 'form']],
            context: {},
            domain: [],
            target: 'inline'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },
    // Function which gives random color for charts.
    getRandomColor: function () {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        //console.log(color)
        return color;
    },
    // Here we are plotting bar,pie chart
    graph: function() {
        var self = this
        var ctx = this.$el.find('#myChart')
        // Fills the canvas with white background
        Chart.plugins.register({
          beforeDraw: function(chartInstance) {
            var ctx = chartInstance.chart.ctx;
            ctx.fillStyle = "white";
            ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
          }
        });
        var bg_color_list = []
        for (var i=0;i<=12;i++){
            bg_color_list.push(self.getRandomColor())
        }

        //Pie Chart - tasks
        var piectx = this.$el.find('#my_tasks_dashboard');
        bg_color_list = []
        for (var i=0;i<=self.employee_data.tasks_dataset.length;i++){
            bg_color_list.push(self.getRandomColor())
        }
        //static color for tasks
        //var bg_static_tasks_color = ['#FF0000','00FF00']
        var pieChart = new Chart(piectx, {
            type: 'pie',
            data: {
                datasets: [{
                    data: self.employee_data.tasks_dataset,
                    backgroundColor: self.employee_data.task_stage_colors,
                    label: 'My Tasks'
                }],
                labels:self.employee_data.tasks_labels,
            },
            options: {
                responsive: true
            }
        });


        //Pie Chart - requests
        var piectt = this.$el.find('#my_requests_dashboard');
        bg_color_list = []
        //for (var i=0;i<=self.employee_data.tasks_dataset.length;i++){
        //    bg_color_list.push(self.getRandomColor())
        //}
        //static color for requests
        //var bg_static_tasks_color = ['#FF0000','00FF00']
        var pieChartt = new Chart(piectt, {
            type: 'pie',
            data: {
                datasets: [{
                    data: self.employee_data.tickets_dataset,
                    backgroundColor: self.employee_data.tickets_stage_colors,
                    label: 'My Requests'
                }],
                labels:self.employee_data.tickets_labels,
            },
            options: {
                responsive: true
            }
        });

         //Pie Chart - investors
        var piectx_i = this.$el.find('#my_investors_dashboard');
        bg_color_list = []
        for (var i=0;i<=self.employee_data.investors_dataset.length;i++){
            bg_color_list.push(self.getRandomColor())
        }
        var pieCharti = new Chart(piectx_i, {
            type: 'pie',
            data: {
                datasets: [{
                    data: self.employee_data.investors_dataset,
                    backgroundColor: bg_color_list,
                    label: 'My Investors'
                }],
                labels:self.employee_data.investors_labels,
            },
            options: {
                responsive: true
            }
        });

        //Pie Chart - companies
        var piectx_c = this.$el.find('#my_companies_dashboard');
        bg_color_list = []
        for (var i=0;i<=self.employee_data.companies_dataset.length;i++){
            bg_color_list.push(self.getRandomColor())
        }
        var pieChartc = new Chart(piectx_c, {
            type: 'pie',
            data: {
                datasets: [{
                    data: self.employee_data.companies_dataset,
                    backgroundColor: bg_color_list,
                    label: 'My Companies'
                }],
                labels:self.employee_data.companies_labels,
            },
            options: {
                responsive: true
            }
        });


        //Pie Chart - projects
        var piectx_p = this.$el.find('#my_projects_dashboard');
        bg_color_list = []
        for (var i=0;i<=self.employee_data.projects_dataset.length;i++){
            bg_color_list.push(self.getRandomColor())
        }
        var pieChartp = new Chart(piectx_p, {
            type: 'pie',
            data: {
                datasets: [{
                    data: self.employee_data.projects_dataset,
                    backgroundColor: bg_color_list,
                    label: 'My Projects'
                }],
                labels:self.employee_data.projects_labels,
            },
            options: {
                responsive: true
            }
        });

    },
    previewTable: function() {
        $('#emp_details').DataTable( {
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel',
                {
                    extend: 'pdf',
                    footer: 'true',
                    orientation: 'landscape',
                    title:'Employee Details',
                    text: 'PDF',
                    exportOptions: {
                        modifier: {
                            selected: true
                        }
                    }
                },
                {
                    extend: 'print',
                    exportOptions: {
                    columns: ':visible'
                    }
                },
            'colvis'
            ],
            columnDefs: [ {
                targets: -1,
                visible: false
            } ],
            lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
            pageLength: 15,
        } );
    },
    generate_payroll_pdf: function(chart) {
        if (chart == 'bar'){
            var canvas = document.querySelector('#myChart');
        }
        else if (chart == 'pie') {
            var canvas = document.querySelector('#attendanceChart');
        }

        //creates image
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('report.pdf');
    },

});
core.action_registry.add('crm_dashboard.dashboard', CRMDashboardView);
return CRMDashboardView
});