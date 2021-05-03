# -*- coding: utf-8 -*-

from odoo import models, fields, multi_process,api, _
from odoo.exceptions import ValidationError


import logging
_logger = logging.getLogger(__name__)


class PortalServicesTms(models.Model):
    _inherit = 'services.tms'

    estado_publicacion = fields.Selection([
        ('oculto','Oculto'),
        ('publicado','Publicado'),
        ('asignado','Asignado'),
        ], string="Estado Publicación")

    metodo_pago = fields.Many2one('metodo.pago.services.tms', string="Metodo de Pago")

    material = fields.Char(string="Material Transportado")

    clientes = fields.Integer(string="Clientes")

    tarifa = fields.Monetary(string="Tarifa")
    currency_id = fields.Many2one('res.currency', string="Moneda", default=19)

    comentarios = fields.Text()

    texto_whatsapp = fields.Text()
    
    link_whatsapp = fields.Text()
    
    link_google_maps = fields.Text()

#    BASE_LINK_WHATSAPP = 'https://wa.me/'

#    @api.onchange('location_load','location_download','date_start')
#    def get_link_whatsapp(self):
#        self.link_whatsapp = self.BASE_LINK_WHATSAPP + self.env.company.phone + '?text=' + 'Bienvenidos a Loyola Transporte, usted esta solicitando la reserva del viaje N°' + self.name



    @api.onchange('employee_third')
    def _get_status_post(self):
        if self.employee_third:
            self.estado_publicacion = 'asignado'
        else:
            self.estado_publicacion = 'publicado'

    def generar_texto_whatsapp(self):
        texto_whatsapp = "***DIFUSIÓN***" + '\n' + "¡¡" + self.material + "!!"

class MetodoPagoPortalServicesTms(models.Model):
    _name = 'metodo.pago.services.tms'

    name = fields.Char(string="Metodo de Pago")

