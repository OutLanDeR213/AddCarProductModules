from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleAutoparts(WebsiteSale):

    @http.route('/add_car_to_product/get_vehicle_models', type='json', auth='public', website=True)
    def get_vehicle_models(self, manufacturer_id=None, **kwargs):
        domain = [('brand_id', '=', int(manufacturer_id))] if manufacturer_id else []
        models = request.env['fleet.vehicle.model'].sudo().search(domain, order='name')
        return [{'id': m.id, 'name': m.name} for m in models]

    def _get_vehicle_params(self):
        args = request.httprequest.args
        return {
            'manufacturer_id': args.get('manufacturer_id'),
            'model_id': args.get('model_id'),
            'year': args.get('year'),
            'volume_id': args.get('volume_id'),
        }

    def _get_vehicle_filter_domain(self):
        if not hasattr(request, '_vehicle_domain_cache'):
            request._vehicle_domain_cache = self._compute_vehicle_domain()
        return request._vehicle_domain_cache

    def _compute_vehicle_domain(self):
        p = self._get_vehicle_params()
        if not any(p.values()):
            return []

        try:
            vehicle_domain = []
            if p['manufacturer_id']:
                vehicle_domain.append(('brand_id', '=', int(p['manufacturer_id'])))
            if p['model_id']:
                vehicle_domain.append(('id', '=', int(p['model_id'])))
            if p['year']:
                y = int(p['year'])
                vehicle_domain += [
                    '&',
                    '|', ('model_year_from', '=', 0), ('model_year_from', '<=', y),
                    '|', ('model_year_to', '=', 0), ('model_year_to', '>=', y),
                ]
            if p['volume_id']:
                vehicle_domain.append(('volume_id', '=', int(p['volume_id'])))
        except (ValueError, TypeError):
            return []

        matching_models = request.env['fleet.vehicle.model'].sudo().search(vehicle_domain)

        products = request.env['product.product'].sudo().search([
            ('is_autoparts', '=', True),
            '|',
            ('compatible_vehicle_ids', 'in', matching_models.ids),
            ('for_all_models', '=', True),
        ])
        tmpl_ids = products.mapped('product_tmpl_id').ids
        return [('id', 'in', tmpl_ids)]

    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        fuzzy_search_term, product_count, search_result = super()._shop_lookup_products(
            attrib_set, options, post, search, website
        )
        vehicle_domain = self._get_vehicle_filter_domain()
        if vehicle_domain:
            search_result = search_result.filtered_domain(vehicle_domain)
            product_count = len(search_result)
        return fuzzy_search_term, product_count, search_result

    def _get_shop_domain(self, search, category, attrib_values, search_in_description=True):
        domain = super()._get_shop_domain(search, category, attrib_values, search_in_description)
        return domain + self._get_vehicle_filter_domain()

    def _get_additional_extra_shop_values(self, values, **post):
        res = super()._get_additional_extra_shop_values(values, **post)
        p = self._get_vehicle_params()

        manufacturer_id = p['manufacturer_id']
        models_domain = [('brand_id', '=', int(manufacturer_id))] if manufacturer_id else []

        res.update({
            'vehicle_manufacturers': request.env['fleet.vehicle.model.brand'].sudo().search([], order='name'),
            'vehicle_models': request.env['fleet.vehicle.model'].sudo().search(models_domain, order='name'),
            'vehicle_volumes': request.env['fleet.vehicle.engine.volume'].sudo().search([], order='name'),
            'selected_manufacturer_id': int(manufacturer_id) if manufacturer_id else None,
            'selected_model_id': int(p['model_id']) if p['model_id'] else None,
            'selected_year': p['year'] or '',
            'selected_volume_id': int(p['volume_id']) if p['volume_id'] else None,
        })
        return res

    def _shop_get_query_url_kwargs(self, category, search, min_price, max_price,
                                   order=None, tags=None, attribute_value=None, **post):
        res = super()._shop_get_query_url_kwargs(
            category, search, min_price, max_price,
            order=order, tags=tags, attribute_value=attribute_value, **post
        )
        res.update(self._get_vehicle_params())
        return res
