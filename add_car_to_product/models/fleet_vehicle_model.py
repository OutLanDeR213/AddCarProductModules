from odoo import fields, models


class FleetVehicleModel(models.Model):
    _inherit = 'fleet.vehicle.model'

    model_year_from = fields.Integer('Year from')
    model_year_to = fields.Integer('Year to')
    model_type = fields.Char('Model type')
    volume_id = fields.Many2one('fleet.vehicle.engine.volume', 'Volume')
    ovoko_car_id = fields.Char('Ovoko car ID')
