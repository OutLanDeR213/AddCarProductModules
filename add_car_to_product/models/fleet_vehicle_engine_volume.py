from odoo import fields, models


class FleetVehicleEngineVolume(models.Model):
    _name = 'fleet.vehicle.engine.volume'
    _description = 'Engine Volume'
    _order = 'name'

    name = fields.Char('Volume (cc)', required=True)
