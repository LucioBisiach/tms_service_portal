# -*- coding: utf-8 -*-


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

        PostsLine = request.env['services.tms']

        post_line_count = PostsLine.sudo().search_count([('estado_publicacion','=','publicado')])

        values['post_line_count'] = post_line_count

        return values


    @http.route(['/my/post_lines', '/my/post_lines/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_post_lines(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()


        PostsLine = request.env['services.tms']

        domain = [('estado_publicacion','=','publicado')]

        searchbar_sortings = {
            'date': {'label': _('Reciente'), 'order': 'create_date desc'},
            'name': {'label': _('Nombre'), 'order': 'name'},
        }

        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('date_start', '>', date_begin)]

        post_line_count = PostsLine.sudo().search_count([('estado_publicacion','=','publicado')])

        pager = portal_pager(
            url="/my/post_lines",
            url_args={'date_begin': date_begin, 'sortby': sortby},
            total=post_line_count,
            page=page,
            step=self._items_per_page
        )

        post_lines = PostsLine.sudo().search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])

        request.session['my_post_lines_history'] = post_lines.ids[:100]

        values.update({
            'date': date_begin,
            'post_lines': post_lines.sudo(),
            'page_name': 'post',
            'pager': pager,
            #'archive_groups': archive_groups,
            'default_url': '/my/post_lines',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })


        return request.render("tms_service_portal.portal_my_post_lines", values)

    @http.route(['/my/post_lines/<int:post_lines_id>'], type='http', auth="user", website=True)
    def post_lines_page(self, post_lines_id=None):

        post_lines = request.env['services.tms'].browse([post_lines_id])

#        logger.warning('[DEBUG #5] values %s'%(service_lines))

        try:
            post_lines.check_access_rights('read')
            post_lines.check_access_rule('read')
        except AccessError:
            return request.website.render('website.403')

        return request.render("tms_service_portal.post_lines_page",{
            'post_lines': post_lines.sudo(),
        })

