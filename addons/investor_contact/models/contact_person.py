# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class contact_person(models.Model):
#     _name = 'contact_person.contact_person'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class ContactPerson(models.Model):
	_name = 'contact.person'
	# _description = 'Model to store contact person records instead of res.partner'
	_inherit = 'res.partner'