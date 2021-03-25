from odoo import models,api,_,fields
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import timedelta
import datetime
from odoo.http import request
from odoo.exceptions import UserError, ValidationError,AccessError
from dateutil import relativedelta


class MailActivityExtend(models.Model):
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
    #         if self.res_id == 0:
    #             new_res_id = max(self.env['mail.activity'].search(['res_id']))

    #         else:
    #             activity.res_name = self.env[activity.res_model].browse(activity.res_id).name_get()[0][1]
    #             activity.res_name = "Prospect Task"
