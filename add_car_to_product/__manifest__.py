{
    'name': 'Add Car to Product',
    'version': '18.0.1.0.0',
    'summary': 'Links fleet vehicle models to products as spare parts',
    'depends': ['fleet', 'product', 'website_sale'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/fleet_vehicle_model_views.xml',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        'views/website_shop_search.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'add_car_to_product/static/src/js/vehicle_search.js',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}
