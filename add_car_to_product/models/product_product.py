from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_autoparts = fields.Boolean(
        'Autopart',
        related='product_tmpl_id.is_autoparts',
        store=True,
    )
    compatible_vehicle_ids = fields.Many2many(
        'fleet.vehicle.model',
        'product_product_vehicle_rel',
        'product_id',
        'vehicle_model_id',
        string='Compatible vehicles',
    )
    for_all_models = fields.Boolean('For all models')
    oem = fields.Char('OEM')
    ovoko_part_id = fields.Char('Ovoko part ID')
