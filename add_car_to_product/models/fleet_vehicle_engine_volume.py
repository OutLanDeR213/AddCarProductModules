from odoo import fields, models


class FleetVehicleEngineVolume(models.Model):
    _name = 'fleet.vehicle.engine.volume'
    _description = 'Engine Volume'
    _order = 'value'

    name = fields.Char('Volume (cc)', required=True)
    value = fields.Integer('Value (cc)', required=True)

    _sql_constraints = [
        ('value_unique', 'UNIQUE(value)', 'This engine volume already exists.'),
    ]
