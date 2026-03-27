{
    'name': 'Custom QR Invoice Base',
    'version': '1.0',
    'depends': ['account', 'stock', 'sale', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/sale_channel_data.xml',
        'views/account_move_views.xml',
        'views/report_invoice_inherit.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'custom_qr_invoice/static/src/xml/pos_customer_list.xml',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}