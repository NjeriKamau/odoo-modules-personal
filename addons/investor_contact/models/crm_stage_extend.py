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


class crm_stage(models.Model):
	_name = 'crm.stage'
	_inherit = 'crm.stage'

	on_change = fields.Boolean('Change Probability Automatically',default=True, help="Setting this stage will change the probability automatically on the opportunity.")
	default_stage = fields.Boolean('Default Stage on Creation')
	is_project = fields.Boolean(string="Needs a Project", help="Select this field if the stage needs a project")
	is_company = fields.Boolean(string="Needs a Company", help="Select this field if the stage needs a company")
	is_inactive = fields.Boolean(string="Inactive Prospect", help="Select this field if the stage is an inactive stage")
	static_state = fields.Boolean(string="Doesn't need a Company or Project", help="Select this field if the stage doesn't need a project or company")


	# def create_project(self):
	# 	if self.is_project == True:
	# 		entity = self.env['project.project'].create({
 #                'name': self.name
 #            })
 #            self.write({
 #                'project_id': entity.id
 #            })

 #        return {
 #            'type': 'ir.actions.act_window',
 #            'name': 'Edit Project Details',
 #            'res_model': 'project.project',
 #            'view_type': 'form',
 #            'view_mode': 'form',
 #            'view_id': self.env.ref('project.edit_project', False).id,
 #            'res_id': entity.id,
 #            'target': 'new',
 #        }