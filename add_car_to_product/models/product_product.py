from odoo import api, fields, models


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

    _sql_constraints = [
        ('ovoko_part_id_unique', 'UNIQUE(ovoko_part_id)',
         'This Ovoko part ID already exists.'),
    ]

    @api.depends(
        'product_tmpl_id.name',
        'is_autoparts',
        'compatible_vehicle_ids',
        'compatible_vehicle_ids.name',
        'compatible_vehicle_ids.brand_id',
        'compatible_vehicle_ids.model_type',
        'compatible_vehicle_ids.model_year_from',
        'compatible_vehicle_ids.model_year_to',
    )
    def _compute_display_name(self):
        autoparts = self.filtered(lambda p: p.is_autoparts and p.compatible_vehicle_ids)
        super(ProductProduct, self - autoparts)._compute_display_name()
        for product in autoparts:
            vehicle = product.compatible_vehicle_ids[0]
            parts = [product.product_tmpl_id.name or '']
            if vehicle.brand_id.name:
                parts.append(vehicle.brand_id.name)
            if vehicle.name:
                parts.append(vehicle.name)
            if vehicle.model_type:
                parts.append(vehicle.model_type)
            if vehicle.model_year_from or vehicle.model_year_to:
                year_from = str(vehicle.model_year_from) if vehicle.model_year_from else ''
                year_to = str(vehicle.model_year_to) if vehicle.model_year_to else ''
                parts.append(f"{year_from}-{year_to}".strip('-'))
            product.display_name = ' '.join(filter(None, parts))
