from odoo import fields, _, api, models
from odoo.exceptions import UserError
from datetime import date,datetime,timedelta


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    _description = "Sales Advance Payment Invoice"




class SaleOrder(models.Model):
    _inherit = "sale.order"
    

    payment_journal = fields.Many2one('account.journal', string='Payment Journal', required=True, readonly=True,ondelete='cascade',
                                 states={'draft': [('readonly', False)]},
                                 check_company=True, domain=[('type', 'in', ('cash', 'bank'))])
    sale_journal_id = fields.Many2one('account.journal', string='Journal', required=True, readonly=True,ondelete='cascade',
                                 states={'draft': [('readonly', False)]},
                                 check_company=True, domain=[('type', '=', 'sale')])

    
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for record in self:
            invoices = record._create_invoices()
            invoices.action_post()
            account_payment_obj = self.env['account.payment']
            for invoice in invoices:
                if invoice.amount_residual:
                    vals = invoice.prepare_payment_dict(record.payment_journal)
                    new_rec = account_payment_obj.create(vals)
                    new_rec.action_post()

                    invoice_journal_items_2 = invoices.line_ids
                    list_of_invoice_journal_items_2 = []
                    for rec in invoice_journal_items_2:
                        list_of_invoice_journal_items_2.append(rec)
                    payment_journal_items_2 = new_rec.move_id.line_ids
                    list_of_payment_journal_items_2 = []
                    for rec in payment_journal_items_2:
                        list_of_payment_journal_items_2.append(rec)
                    combined_journal_list_2 = list_of_invoice_journal_items_2 + list_of_payment_journal_items_2
                    account_move_lines_to_reconcile = self.env['account.move.line']
                    for line in combined_journal_list_2:
                        if line.account_id.account_type == 'asset_receivable':
                            account_move_lines_to_reconcile |= line
                    account_move_lines_to_reconcile.reconcile()
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        journal = self.order_id.sale_journal_id
        if journal:
            res.update({'account_id': journal.default_account_id.id})
        return res