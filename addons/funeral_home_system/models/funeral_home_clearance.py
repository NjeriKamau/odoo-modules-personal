# -*- coding: utf-8 -*-

from odoo import models,fields,api,_


import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as dt
from odoo.exceptions import ValidationError, UserError
import pytz



# class FuneralClearance(models.Model):

class FuneralClearance(models.Model):
    

    _name = 'funeral_home.clearance'
    _inherit = ['mail.thread']
    _description = 'Funeral home clearance'
    _rec_name = "fh_admission_tag_no"

    # _rec_name = ''
    # _order = ''

    fh_date_of_dispatch = fields.Datetime('Date of dispatch',readonly=True, required=True, index=True, default=(lambda *a: time.strftime(dt)))

    fh_admission_tag_no= fields.Many2one('funeral_home.admission', string='Admission/Tag. No') # database identifier of the record to set
    # fh_admission_tag_no= fields.Char(string='Admission/Tag. No', readonly=True) # database identifier of the record to set

    date_fh_order = fields.Datetime(comodel_name='funeral_home.admission', string='Date')
    fh_id_passport_of_deceased = fields.Char(string='ID/Passport of deceased')
    # fh_name_of_deceased = fields.Char(string='Name of deceased',readonly=True, required=True, store=True)
    fh_name_of_deceased = fields.Char(string='Name of deceased', related='fh_admission_tag_no.fh_name_of_deceased', readonly=True, store=True)
    # fh_name_of_deceased = fields.Char(string='Name of deceased', readonly=True, store=True)

    # fh_name_of_kin = fields.Many2one(comodel_name='funeral_home.admission', ondelete='restrict', delegate=True, string='Name of Kin')
    # fh_id_passport_of_kin = fields.Many2one(comodel_name='funeral_home.admission', ondelete='restrict', delegate=True, string='ID/Passport of Kin')
    # fh_relationship_with_deceased = fields.Many2one(comodel_name='funeral_home.admission', ondelete='restrict', delegate=True, string='Relationship wth deceased')
    # fh_telephone_contact_kin = fields.Many2one(comodel_name='funeral_home.admission', ondelete='restrict', delegate=True, string='Telephone contact of kin.')
    fh_destined_county = fields.Char('Destination County', size=40, help="What needs to be done?",required=True)
    fh_destined_subcounty = fields.Char('Destination Sub-County', size=40, help="What needs to be done?",required=True)
    fh_destined_location = fields.Char('Location', size=40, help="What needs to be done?",required=True)
    fh_nearest_police_post = fields.Char('Police Station', size=40, help="What needs to be done?",required=True)
    fh_nearest_landmark = fields.Char('Nearest Landmark', size=40, help="What needs to be done?",required=True)

    fh_burial_permit_number = fields.Char('Burial permit number', size=20, help="Burial permit number")
    # fh_invoice_number = fields.Many2one(comodel_name='funeral_home.admission', ondelete='restrict', delegate=True)
    fh_amount = fields.Float(digits=(6, 2), string='Amount')
    fh_waived_amount = fields.Float(compute="_waiver_pc", store=True, string='Waived Amount')

    fh_admission_ids = fields.Many2one('funeral_home.admission', string="Admissions Link")
    fh_kin_details = fields.Many2many('funeral_home.admission',relation='admission_clearance_link', column1='fh_admission_ids',column2='fh_clearance_link', string='Kin Details')
    # fh_kin_details = fields.Many2many('funeral_home.admission', string='Kin Details')

    # states
    state = fields.Selection([
        ('draft', "Draft"),
        ('open', "Open"),
        ('paid', "Paid"),
        ], default='draft')

    @api.depends('fh_amount')
    def _waiver_pc(self):
    	self.fh_waived_amount = float(self.fh_amount) / 100
    

    # @api.model
    # def write(self, vals):
    #     vals['fh_name_of_deceased'] = self.env['funeral_home.admission'] \
    #         .browse(vals['fh_admission_tag_no']) \
    #         .fh_name_of_deceased
    #     return super(FuneralClearance, self).create(vals)


    # update client details
    # def write(self, vals):
    #     if 'fh_admission_tag_no' in vals:
    #         print(vals)
    #         vals['fh_name_of_deceased'] = self.env['funeral_home.admission'] \
    #             .browse(vals['fh_admission_tag_no']) \
    #             .fh_name_of_deceased
    #     return super(FuneralClearance, self).write(vals)


    # @api.onchange('fh_admission_tag_no')
    # def onchange_admission_tag_no(self):
    #     '''
    #     When you change fh_admission_tag_no it will update date_fh_order,
    #     fh_name_of_deceased as well as the kins of the deceased
    #     ---------------------------------------------------------------------
    #     @param self: object pointer
    #     '''
    #     fh_admission_rec = self.env['funeral_home.admission'].browse(self.fh_admission_tag_no.id)
    #     if self.fh_admission_tag_no:
    #         self.fh_admission_tag_no = fh_admission_rec.id
    #         self.fh_name_of_deceased = fh_admission_rec.fh_name_of_deceased
    #         self.date_fh_order = fh_admission_rec.date_fh_order

    #     return fh_admission_rec



    def action_cancel(self):
        self.state = 'draft'


    def action_confirm(self):
        self.state = 'open'


    def action_invoice(self):
        self.state = 'paid'

    def action_mail_receipt(self):
        self.state = 'paid'

    def action_receipt(self):
        self.state = 'paid'

    # @api.multi
    # def action_clear(self):
    #     self.state = 'done'