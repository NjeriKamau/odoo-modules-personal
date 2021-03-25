# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    investor_team_id = fields.Many2one(
        'crm.lead', 'Investment Team',
        help='Investment Team Creation')
