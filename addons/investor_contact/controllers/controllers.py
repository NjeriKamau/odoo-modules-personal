import json
from odoo import http
from odoo.http import request, Response

class Teams(http.Controller):
	
    @http.route('/titles/', type="json", auth="none", csrf=False)
    def titles(self):
        res = []
        for title in http.request.env['res.partner.title'].sudo().search([]):
            res.append({'name': title.shortcut, 'id': title.id})

        return res

    @http.route('/sectors/', type="json", auth="none", csrf=False)
    def sectors(self):
        res = []
        for sector in http.request.env['res.partner.industry'].sudo().search([('active', '=', 'True')]):
            res.append({'name': sector.name, 'id': sector.id})

        return res

    @http.route('/country/', type="json", auth="none", csrf=False)
    def country(self):
        res = []
        for country in http.request.env['res.country'].sudo().search([]):
            res.append({'name': country.name, 'id': country.id})

        return res

class WebsiteController(http.Controller):
    
    @http.route('/website_form_override/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
        res = http.request.env[model_name].sudo().create({
                'itype': 'Email In',
                'cert': request.params.get('cert'),
                'tin': request.params.get('tin'),
                'type_invest': request.params.get('type_invest'),
                'project_description': request.params.get('project_description'),
                'start_date': request.params.get('start_date'),
                'investment_amount': request.params.get('investment_amount'),
                'p_job_creation': request.params.get('p_job_creation'),
                'p_address': request.params.get('p_address'),
                'sector': request.params.get('sector'),
                'city': request.params.get('city'),
                'state': request.params.get('state'),
                'partner_name': request.params.get('partner_name'),
                'title': request.params.get('title'),
                'contact_name': request.params.get('contact_name'),
                'function': request.params.get('function'),
                'email_from': request.params.get('email_from'),
                'phone': request.params.get('phone'),
                'sector': request.params.get('sector'),
                'name': request.params.get('name'),
                'country_id': request.params.get('country_id')
        })

        return Response(json.dumps({'id': res.id}))
