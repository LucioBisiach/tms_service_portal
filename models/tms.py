# -*- coding: utf-8 -*-

from odoo import models, fields, multi_process,api, _
from odoo.exceptions import ValidationError


import logging
_logger = logging.getLogger(__name__)


class PortalServicesTms(models.Model):
    _inherit = 'services.tms'


    metodo_pago = fields.Many2one('metodo.pago.services.tms', string="Metodo de Pago")

    material = fields.Char(string="Material Transportado")

    clientes = fields.Integer(string="Clientes")

    tarifa = fields.Float(string="Tarifa")

    comentarios = fields.Text()


class MetodoPagoPortalServicesTms(models.Model):
    _name = 'metodo.pago.services.tms'

    name = fields.Char(string="Metodo de Pago")

