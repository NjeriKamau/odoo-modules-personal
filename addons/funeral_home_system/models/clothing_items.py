
from odoo import models, fields, api


class Clothingitems(models.Model):
	_name='funeral_home.clothing.particulars'
	_inherit = ['mail.thread']
	_description="Values forn the clothes"


	clothe_name= fields.Char('Clothe Name', size=30, required=True)
	description=fields.Char('Item Description', required=True)
