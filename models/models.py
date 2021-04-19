# -*- coding: utf-8 -*-

from odoo import models, fields, multi_process,api, _
from odoo.exceptions import ValidationError



import logging
_logger = logging.getLogger(__name__)

class ResGroupsTMS(models.Model):
    _inherit = 'res.users'


    def get_driver_user(self):
        lst_categorias = []


        for categoria in self.partner_id.category_id:
            lst_categorias.extend([categoria.name]) 

        if "Chofer" in lst_categorias and "Administrador Logistico" in lst_categorias:
            _logger.info("es Adm Logistico")
            for obj in self.groups_id.model_access:
                obj.perm_read = True

        if "Chofer" in lst_categorias and "Administrador Logistico" not in lst_categorias:
            _logger.info("Es solo Chofer")
            for obj in self.groups_id.model_access:
                if not obj.name == 'access.tms.services.portal' and not obj.name == 'document.page portal' and not obj.name == 'res_partner group_portal':
                    obj.perm_read = False
                else:
                    obj.perm_read = True
                _logger.info("Grupos: %s", obj.name)
        else:
            #if "Administrador Logistico" in lst_categorias and "Chofer" not in
            _logger.info("Es solo Adm Logistico")
            for obj in self.groups_id.model_access:
                obj.perm_read = True


