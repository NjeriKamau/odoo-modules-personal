# -*- coding: utf-8 -*-

from openerp import models, fields, api

class HearseBooking(models.Model):
    _name = 'funeral_home.hearse.booking'
    _inherit = ['mail.thread']
    _description='Hearse Booking Records'


    # client_name = fields.Char()
    # adm_no = fields.Char()
    fh_admission_tag_no= fields.Many2one(comodel_name='funeral_home.admission', delegate=True, string='Admission/Tag. No', required='True')
    fh_name_of_deceased= fields.Char(readonly=True, string='Name of Deceased', related='fh_admission_tag_no.fh_name_of_deceased')
    booking_date = fields.Datetime()
    venue = fields.Char(string="Venue")
    # should only pick up date
    burial_date = fields.Datetime()
    # should only pick up time
    burial_day = fields.Datetime()
    burial_location = fields.Char()
    near_market = fields.Char()
    # distance --> try to see how to use Google Maps for this
    distance = fields.Char()
    service = fields.Selection([('Yes','Yes'), ('No','No')])
    # should be retrieved from google maps to enhance accuracy
    service_locale = fields.Char()
    person_booking = fields.Char()
    person_id = fields.Char()
    relationship = fields.Char()
    # find out if there's a phone number field
    tel_no = fields.Char()
    # should pick up time only
    dispach_time = fields.Datetime()
    signature = fields.Char()


# retrieve the client name from admission model
    # @api.onchange('fh_admission_tag_no','') 
    # def onchange_admission_tag_no(self):
    #     '''
    #     When you change fh_admission_tag_no it will update date_fh_order,
    #     fh_name_of_deceased as well as the kins of the deceased
    #     ---------------------------------------------------------------------
    #     @param self: object pointer
    #     '''
    #     if self.fh_admission_tag_no:
    #         fh_admission_rec = self.env['funeral_home.admission'].browse(self.fh_admission_tag_no.id)
    #         # fh_name_of_deceased_rec = self.env['funeral_home.admission'].browse(self.fh_name_of_deceased.id)

    #         self.fh_admission_tag_no = fh_admission_rec.id
    #         self.fh_name_of_deceased = fh_admission_rec.fh_name_of_deceased
    #         self.booking_date = fh_admission_rec.date_fh_order

