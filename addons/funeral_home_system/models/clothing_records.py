
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime


class Clientclothes(models.Model):
    _name='funeral_home.client.clothes'
    _inherit = ['mail.thread']
    # _inherit='clothing.particulars'
    _description='Record of client clothing'


    reg_no=fields.Many2one(comodel_name='funeral_home.admission', delegate=True, string='Admission/Tag. No', required='True') # database identifier of the record to set


    # def _get_client_name(self):
    #     active_id=self.env['funeral_home.admission'].browse(self.id)
    #     if active_id != False:
    #         return active_id.fh_name_of_deceased

    client_name=fields.Char(string='Name of deceased',readonly=True, store=True)
    depart_date=fields.Datetime("Date and Time of Departure", required='True')
    # depart_time=fields.Datetime("Time of Departure")
    #  default=lambda *a: datetime.now('%H:%M')
    coffin_type=fields.Char('Coffin Type and Color')
    cross_type=fields.Char('Cross Type and Color')
    supplier=fields.Char('Supplier')
    clothing_items=fields.Many2many('funeral_home.clothing.particulars','funeral_home_clothe_name')

    baby_wear=fields.Char("Baby's Wear (Please Specify)")
    # optional, but necessary, to allow filtring of records in clothing_selection

    # extra fields, for completeing the form before integration with the main system.
    del_relative=fields.Char(size=30, string="Name of Delivering Relative.")
    rel_date=fields.Date('Date of Delivery')
    receive_officer=fields.Char(size=30, string="Name of Recieving Officer.")
    receive_date=fields.Date('Date of Reception')
    

    @api.model
    def create(self, vals):
        vals['fh_name_of_deceased'] = self.env['funeral_home.admission'].browse(vals['reg_no']).fh_name_of_deceased
        return super(Clientclothes, self).create(vals)


    # update client details
    def write(self, vals):
        if 'reg_no' in vals:
            vals['fh_name_of_deceased'] = self.env['funeral_home.admission'].browse(vals['reg_no']).fh_name_of_deceased
        return super(Clientclothes, self).write(vals)


    @api.onchange('reg_no')
    def onchange_admission_tag_no(self):
        '''
        When you change fh_admission_tag_no it will update date_fh_order,
        fh_name_of_deceased as well as the kins of the deceased
        ---------------------------------------------------------------------
        @param self: object pointer
        '''
        fh_admission_rec = self.env['funeral_home.admission'].browse(self.reg_no.id)
        if self.reg_no:
            self.reg_no = fh_admission_rec.id
            self.fh_name_of_deceased = fh_admission_rec.fh_name_of_deceased
            self.date_fh_order = fh_admission_rec.date_fh_order

        return fh_admission_rec


