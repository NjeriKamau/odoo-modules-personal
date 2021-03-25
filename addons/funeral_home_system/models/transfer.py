# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as dt
import time
from datetime import datetime, timedelta


class Transfer(models.Model):
	_name = 'funeral_home.transfer'
	_inherit = ['mail.thread']
	_description = 'Record Transfer Details'

	fh_admission_tag_no= fields.Many2one('funeral_home.admission', string='Admission/Tag. No', required=True ) # database identifier of the record to set
	deceased_name_transfer = fields.Char('Name of deceased', related='fh_admission_tag_no.fh_name_of_deceased', readonly=True, store=True)
	fh_institution_of_origin = fields.Many2one('res.company', string='Institution of Origin', size=40, help="Institution of origin, e.g. Hospital, Another funeral home, e.t.c.")
	date_transfer = fields.Datetime('Date ',readonly=True, required=True, index=True, default=(lambda *a: time.strftime(dt)))	
	fh_transfer_person = fields.Many2one('res.partner', string="Person seeking transfer services...")