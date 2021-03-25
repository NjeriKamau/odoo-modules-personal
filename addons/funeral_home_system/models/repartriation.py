# -*- coding: utf-8 -*-

from openerp import models, fields, api
import time
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as dt


class Repatriation(models.Model):
    _name = 'funeral_home.repatriation'
    _inherit = ['mail.thread']
    _rec_name = 'fh_repartriation_tag_no'
    _description = 'Repartriation Records'
    # _inherit = 'funeral_home.admission'

    fh_repartriation_tag_no = fields.Char('Admission/Tag No', readonly=True)
    deceased_name_repatriation = fields.Char('Name of deceased', size=40, help="Name of deceased.")
    fh_country_of_origin = fields.Many2one('res.country', string="Country of Origin")
    date_repatriation = fields.Datetime('Date ',readonly=True, required=True, index=True, default=(lambda *a: time.strftime(dt)))
    fh_airline = fields.Many2one('res.company', string='Airline', size=40, help="Transportation Airline")
    fh_repatriation_person = fields.Many2one('res.partner', string="Person seeking services...")
    upload_file = fields.Binary(string="Upload File")
    file_name = fields.Char(string="File Name")

    state = fields.Selection([
        ('draft', "Draft"),
        ('approval', "Approval"),
        ('open', "Open"),
        ('paid', "Paid"),
    ], default='draft')
    
    @api.model
    def create(self, vals):
        seq_obj = self.env['ir.sequence']
        vals['fh_repartriation_tag_no'] = seq_obj.next_by_code('funeral_home.repatriation') or 'New'
        return super(Repatriation, self).create(vals)


    def action_request(self):
        self.state = 'approval'


    def action_cancel(self):
        self.state = 'draft'

    def action_invoice(self):
        self.state = 'open'


    def action_payment(self):
        self.state = 'paid'

    def action_mail_receipt(self):
        self.state = 'paid'
        
    def action_receipt(self):
        self.state = 'paid'
