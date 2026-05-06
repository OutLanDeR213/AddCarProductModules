from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class FleetVehicleModel(models.Model):
    _inherit = 'fleet.vehicle.model'

    model_year_from = fields.Integer('Year from')
    model_year_to = fields.Integer('Year to')
    model_type = fields.Char('Model type')
    volume_id = fields.Many2one('fleet.vehicle.engine.volume', 'Volume')
    ovoko_car_id = fields.Char('Ovoko car ID')

    _sql_constraints = [
        ('ovoko_car_id_unique', 'UNIQUE(ovoko_car_id)',
         'This Ovoko car ID already exists.'),
    ]

    @api.constrains('model_year_from', 'model_year_to')
    def _check_years(self):
        for rec in self:
            if rec.model_year_from and rec.model_year_to:
                if rec.model_year_from > rec.model_year_to:
                    raise ValidationError(_('Year from cannot be greater than Year to.'))
