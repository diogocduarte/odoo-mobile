    

class sale_order(osv.osv):
    _inherit = "account.invoice"
    # ...
    def zimbra_close_invoice(self, cr, uid, email, code, context=None):

        """
        this is a conceptual example
        
        code for closing invoice
        double validation code and email
        using CGD Bank journal
        """
        
        res = {
               'success': True,
               # just review closed invoice
               'next_action_button': {
                            'domain':[('...','=','...')],
                            'view_mode': 'tree,form,calendar,graph',
                            'res_model': 'account.invoice',
                            'search_view_id': ('account....'),
                            },
               # in case we need to postpone to user selection
               'select_partner_domain': [('...','=','...')],
               'select_journal_domain': [('...','=','...')],
        }
        
        """
        def zimbra_close_invoice(self, cr, uid, email, code, partner_id=False, context=None ):
        """
        
        return res