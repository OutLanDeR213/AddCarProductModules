from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_autoparts = fields.Boolean('Is Autopart')
