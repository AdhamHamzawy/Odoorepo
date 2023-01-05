from odoo import fields, _, api, models
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta


class AccountMove(models.Model):
    _inherit = "account.move"

   
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, readonly=True,ondelete='cascade',
                                 states={'draft': [('readonly', False)]},
                                 check_company=True, domain="[('id', 'in', suitable_journal_ids)]")

    def prepare_payment_dict(self, payment_journal):
        """
        Added By Udit
        This method will prepare payment dictionary.
        :param work_flow_process_record: It is work flow object.
        """
        return {
            'journal_id': payment_journal.id,
            'reconciled_invoice_ids': [(6, 0, [self.id])],
            'currency_id': self.currency_id.id,
            'payment_type': 'inbound',
            'date': self.date,
            'partner_id': self.partner_id.id,
            'amount': self.amount_residual,
            'payment_method_line_id': payment_journal.inbound_payment_method_line_ids.payment_method_id.id,
            'partner_type': 'customer'
        }


