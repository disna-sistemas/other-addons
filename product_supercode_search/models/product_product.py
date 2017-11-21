
from openerp import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _rec_name = 'supercode'

    @api.multi
    @api.depends('default_code', 'name', 'ean13',
                 'customer_ids.name.ref',
                 'customer_ids.product_code',
                 'supplier_ids.name.ref',
                 'supplier_ids.product_code')
    def _update_supercode(self):
        for product in self:
            val = []
            for supplier in product.supplier_ids:
                val += [supplier.name.name, (supplier.name.ref or ''),
                        (supplier.product_code or '')]
            for customer in product.customer_ids:
                val += [customer.name.name, (customer.name.ref or ''),
                        (customer.product_code or '')]
            if product.default_code:
                val.append(product.default_code)
            if product.name:
                val.append(product.name)
            if product.ean13:
                val.append(product.ean13)
            product.supercode = " ".join(val)

    supercode = fields.Char(string='Supercode', store=True,
                            compute="_update_supercode")

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        return models.Model.name_search(self, name=name, args=args,
                                        operator=operator, limit=limit)
