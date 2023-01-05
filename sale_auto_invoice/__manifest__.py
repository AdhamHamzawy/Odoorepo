# -*- coding: utf-8 -*-
{
    'name': "Sales Auto Invoice",

    'author': "Adham Hamzawy",
     'description': """
        after confirming sale order the rest of the process will be confirmed ,
        ( sale order state will be confirmed ,  delivery order confirmed , invoice created ,
        invoice payment done ) in one button click
    """,
    # any module necessary for this one to work correctly 
    
    'depends': ['base', 'sale', 'account'],
    'version': '16',
    # always loaded
    'data': [
        'views/sale_view.xml',

    ],
}
