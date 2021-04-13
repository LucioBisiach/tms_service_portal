# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import binascii
from datetime import date

from odoo import fields, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.osv import expression
import logging

logger = logging.getLogger(__name__)



class CustomerPortal(CustomerPortal):


    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()

        # Pregunta si el usuario pertenece a una compañia (Esto nos diferencia entre individuo y compañia)
        if request.env.user.partner_id.parent_id:
            # Pasa el parametro de la compañia a la que pertenece si es un usuario
    	    partner_id = request.env.user.partner_id.parent_id
            #logger.warning('[DEBUG #2] values %s'%(partner_id))
        else:
            # En caos de que no pertenezca a ninguna compañia, imprime el ID de la compañia
            partner_id = request.env.user.partner_id
            #logger.warning('[DEBUG #3] values %s'%(partner_id))

        ServiceLine = request.env['services.tms']
        services_line_count = ServiceLine.sudo().search_count([('supplier', '=', partner_id.id)])

        values['services_line_count'] = services_line_count
        # logger.warning('[DEBUG #5 values %s'%(services_line_count))
        return values



    @http.route(['/my/service_lines', '/my/service_lines/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_service_lines(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        # logger.warning('[DEBUG #2 values %s'%(values)) 

        partner = request.env.user.partner_id
        ServiceLine = request.env['services.tms']

        if request.env.user.partner_id.parent_id:
            partner_id = request.env.user.partner_id.parent_id
        else:
            partner_id = request.env.user.partner_id

        domain = [('supplier', '=', partner_id.id)]

        searchbar_sortings = {
            'name': {'label': _('date_start'), 'order': 'name'},
        }

        if not sortby:
            sortby = 'name'
        sort_order = searchbar_sortings[sortby]['label']

        #archive_groups = self.sudo()._get_archive_groups('account.debt.line', domain)
        if date_begin and date_end:
            domain += [('date_start', '>', date_begin), ('date_end', '<=', date_end)]


        # count for pager
        service_line_count = ServiceLine.sudo().search_count(domain)


        pager = portal_pager(
            url="/my/service_line",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=service_line_count,
            page=page,
            step=self._items_per_page
        )

        service_lines = ServiceLine.sudo().search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_service_lines_history'] = service_lines.ids[:100]

        values.update({
            'date': date_begin,
            'service_lines': service_lines.sudo(),
            'page_name': 'service',
            'pager': pager,
            #'archive_groups': archive_groups,
            'default_url': '/my/service_lines',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })

        #logger.warning(values)
        return request.render("tms_service_portal.portal_my_service_lines", values)



    @http.route(['/my/service_line/<int:service_lines>'], type='http', auth="user", website=True)
    def service_lines_page(self, service_lines=None, ):
        service_lines = request.env['services.tms'].browse([service_lines])
        #logger.warning('SERVICE LINES /MY/SERVICE_LINES %s'%(service_lines))

        try:
            service_lines.check_access_rights('read')
            service_lines.check_access_rule('read')
        except AccessError:
            return request.website.render('website.403')

        return request.render("tms_service_portal.service_lines_page",{
            'service_lines': service_lines.sudo(),
        })
