# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as dt
from odoo.exceptions import ValidationError, UserError
import pytz


class FuneralAdmission(models.Model):

    def create_clearance(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create a Clearance Request',
            'res_model': 'funeral_home.clearance',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'view_id': self.env.ref('funeral_home_system.view_funeral_home_clearance_form').id,
            # 'context':{},
            'context': {
                # 'default_fh_admission_ids': self.id,
                # 'default_fh_kin_details': [(4, self.fh_kin_details)],
                'default_fh_kin_details': (self.fh_kin_details.ids),
                'default_fh_admission_tag_no': self.fh_admission_tag_no,
                'default_fh_name_of_deceased':self.fh_name_of_deceased,
                'default_fh_id_passport_of_deceased':self.fh_id_passport_of_deceased,
                


            },
        }

    _name = "funeral_home.admission"
    _inherit = ['mail.thread']
    _rec_name = "fh_admission_tag_no"
    _order = 'id'
    _description='Record of Client Admission'

    fh_name_of_deceased = fields.Char('Name of deceased', required=True, size=40, help="looking for words that mean:something")
    fh_admission_tag_no = fields.Char('Admission/Tag No', readonly=True)
    date_fh_order = fields.Datetime('Date ', readonly=True, required=True, index=True,
                                    default=(lambda *a: time.strftime(dt)))
    fh_client_age = fields.Integer('Client age', compute='_get_client_age', store=True)
    
    fh_id_passport_of_deceased = fields.Char(string='ID/Passport of deceased')

    date_fh_of_death = fields.Date(string='Date of death', required=True, index=True,
                                   default=(lambda *a: time.strftime(dt)))
    date_fh_of_birth = fields.Date(string='Date of birth', required=True, index=True,
                                   default=(lambda *a: time.strftime(dt)))
    fh_client_sex = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender',
                                     help="looking for words that mean:something")
    fh_place_of_death = fields.Char('Place of death', size=40, help="looking for words that mean:something")
    fh_nature_of_death = fields.Text('Nature of death', help="looking for words that mean:something")
    # fh_name_of_kin = fields.Char('Name of Kin', size=40, help="looking for words that mean:something")
    # fh_id_passport_of_kin = fields.Char('ID/Passport', size=8, help="looking for words that mean:something")
    # fh_telephone_contact_kin = fields.Integer("Kin's telephone contact", size=12,
    #                                           help="looking for words that mean:something")
    # fh_relationship_with_deceased = fields.Char('Relationship with deceased', size=32,
    #                                             help="looking for words that mean:something")
    fh_place_body_from = fields.Char('Place from', size=40, help="looking for words that mean:something")
    fh_postmortem_interval = fields.Selection([('1', 'One day'), ('two', 'Two days')], 'Postmortem interval',
                                              help ="looking for words that mean:something")
    fh_postmortem_done = fields.Boolean('Postmortem done?', help="looking for words that mean:something")
    fh_forensic_case = fields.Boolean('Forensic case?', help="looking for words that mean:something")
    fh_preservation_and_storage = fields.Boolean('Preservation and storage?',
                                                 help="looking for words that mean:something")
    fh_postmortem = fields.Boolean('Postmortem?', help="looking for words that mean:something")
    fh_reconstruction = fields.Boolean('Reconstruction?', help="looking for words that mean:something")
    fh_cosmetics = fields.Boolean('Cosmetics?', help="looking for words that mean:something")
    fh_other_services = fields.Text('Other services', help="looking for words that mean:something")

    fh_kin_details = fields.Many2many('res.partner', string='Kin details', help='Kin details.')

    fh_kins_count = fields.Integer(string="Kins count", compute='_get_kins_count', store=True)
    fh_clearance_link = fields.Many2one('funeral_home.clearance', string='Clearance Model Link')

    
    # _rec_name = "(fh_admission_tag_no) fh_name_of_deceased"
    # @api.multi
    # def name_get(self):
    #     result = []
    #     for record in self:
    #         result.append("(%s) %s" % (record.fh_admission_tag_no, record.fh_name_of_deceased))
    #     return result
    
    @api.model
    def create(self, vals):
        """
        Overrides orm create method.
        @param self: The object pointer
        @param vals: dictionary of fields value.
        """
        if vals.get('fh_admission_tag_no', 'New') == 'New':
            vals['fh_admission_tag_no'] = self.env['ir.sequence'].next_by_code(
                'funeral_home.admission') or 'New'
        return super(FuneralAdmission, self).create(vals)
  
        # seq_obj = self.env['ir.sequence']
        # vals['fh_admission_tag_no'] = seq_obj.next_by_code('funeral_home.admission') or 'New'
        # return super(FuneralAdmission, self).create(vals)

    # update client age
    def write(self, vals):
        vals['fh_client_age'] = self._get_date_diff(
            vals.get('date_fh_of_death', self.date_fh_of_death), 
            vals.get('date_fh_of_birth', self.date_fh_of_birth)
        )
        return super(FuneralAdmission, self).write(vals)

    # calculate client age
    @api.onchange('date_fh_of_birth', 'date_fh_of_death')
    def _get_client_age(self):
        self.fh_client_age = self._get_date_diff(self.date_fh_of_death, self.date_fh_of_birth)

    
    def _get_date_diff(self, start, end):
        start = datetime.strptime(str(start), '%Y-%m-%d')
        end = datetime.strptime(str(end), '%Y-%m-%d')
        return relativedelta(start, end).years


    # minimum number of Kins is three
    @api.depends('fh_kin_details')
    def _get_kins_count(self):
        print("self.fh_kin_details.ids........")
        print(self.fh_kin_details.ids)
        for r in self:
            r.fh_kins_count = len(r.fh_kin_details)
            if r.fh_kins_count < 3:
                raise exceptions.ValidationError("Please add three or more next-of-kins!")
