from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_autoparts = fields.Boolean('Is Autopart')

    def action_open_autopart_variants(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Autopart Variants',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('product_tmpl_id', '=', self.id)],
            'context': {'default_product_tmpl_id': self.id},
        }
