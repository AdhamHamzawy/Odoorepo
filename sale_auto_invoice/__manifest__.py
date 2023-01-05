# -*- coding: utf-8 -*-
{
    'name': "Sales Auto Invoice",

    'author': "Adham Hamzawy",

    # any module necessary for this one to work correctly 
   # odoo16
    'depends': ['base', 'sale', 'account'],

    # always loaded
    'data': [
        'views/sale_view.xml',

    ],
}
