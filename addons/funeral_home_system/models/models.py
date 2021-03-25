# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class funeral_home_system(models.Model):
#     _name = 'funeral_home_system.funeral_home_system'
#     _description = 'funeral_home_system.funeral_home_system'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
