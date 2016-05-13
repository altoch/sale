# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class SaleInvoiceOperation(models.Model):
    _inherit = 'account.invoice.operation'
    _name = 'sale.invoice.operation'

    # only required on invoice operation, not in sale operations
    invoice_id = fields.Many2one(
        required=False,
        auto_join=True,
    )
    order_id = fields.Many2one(
        'sale.order',
        'Sale Order',
        auto_join=True,
        ondelete='cascade',
        required=True,
    )

    @api.one
    @api.constrains('order_id', 'journal_id', 'company_id')
    def check_currencies(self):
        other_currency = (
            self.journal_id.currency or self.company_id.currency_id)
        if other_currency and self.order_id.currency_id != other_currency:
            raise Warning(_(
                'You can not use a journal or company of different currency '
                'than sale order currency. Operation "%s"') % (
                    self.display_name))

    @api.one
    @api.constrains('order_id', 'percentage')
    def check_percetantage(self):
        orders = self.search(
            [('order_id', '=', self.order_id.id)])
        if sum(orders.mapped('percentage')) > 100.0:
            raise Warning(_(
                'Sum of percentage could not be greater than 100%'))