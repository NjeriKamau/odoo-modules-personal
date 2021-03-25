# -*- coding: utf-8 -*-

import time

from odoo import models, fields, api


class ResUser(models.Model):
    # Change model to employee module
    _inherit = 'res.users'

    fh_debrief = fields.One2many('funeral_home.debrief', 'employee', 'Employee')
    fh_immunisation = fields.One2many('funeral_home.immunisation', 'employee', 'Employee')


class FuneralDeBrief(models.Model):
    _name = "funeral_home.debrief"
    _rec_name = "employee"
    _order = 'id'

    employee = fields.Many2one('res.users', 'Employee', ondelete='cascade')
    visit = fields.Datetime('Review Date ', required=True)
    comments = fields.Text('Comments', help="A brief summary of the observations made.")


class FuneralImmunisation(models.Model):
    _name = "funeral_home.immunisation"
    _rec_name = "employee"
    _order = 'id'

    VACCINE_ROUTES = [
        ('IM', 'Intramuscular'),
        ('SC', 'Subcutaneous'),
        ('ID', 'Intradermal'),
        ('NAS', 'Intranasal'),
        ('PO', 'Oral'),
    ]

    VACCINE_SITES = [
        ('RA', 'Right Arm'), 
        ('LA', 'Left Arm'), 
        ('RT', 'Right Thigh'), 
        ('LT', 'Left Thigh')
    ]

    employee = fields.Many2one('res.users', 'Employee', ondelete='cascade')
    vaccine_type = fields.Char('Type of Vaccine', size=250)
    route = fields.Selection(VACCINE_ROUTES, 'Route', help='the route by which the vaccine was given')
    site = fields.Selection(VACCINE_SITES, 'Site', help='where the vaccine was administered')
    lot_no = fields.Char('Lot #', size=250, help='The lot number associated with the vaccine')
    date_on_vis = fields.Datetime('Date on VIS')
    date_given = fields.Datetime('Date Given', required=True)
