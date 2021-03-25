from odoo import models, fields, api


class Freezer(models.Model):
    _name = 'funeral_home.freezer'
    _inherit = ['mail.thread']
    _rec_name = 'model_name'

    model_name = fields.Char('Fridge Label', size=40)
    trays = fields.One2many('funeral_home.freezer.tray', 'freezer', 'Tray List')


class FreezerTray(models.Model):
    _name = 'funeral_home.freezer.tray'
    _inherit = ['mail.thread']
    _rec_name = 'tray_slug'

    freezer = fields.Many2one('funeral_home.freezer', 'Freezer', ondelete='cascade')
    tray_slug = fields.Char('Slug', size=40)
    occupied = fields.Boolean('Occupied')