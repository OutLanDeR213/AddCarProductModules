{
    'name': 'Add Car to Product',
    'version': '18.0.1.0.0',
    'summary': 'Links fleet vehicle models to products as spare parts',
    'depends': ['fleet', 'product', 'website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/fleet_vehicle_model_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
