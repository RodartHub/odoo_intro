{
    'name': "Estate",
    'version': '1.0',
    'author': "Rodrigo",
    'depends': [
        'base',
        'web',
    ],
    'data':[
        'security/ir.model.access.csv',
        'views/estate_menu.xml',
        'views/estate_property_view.xml',
        'views/estate_property_offers_view.xml',
        'views/estate_property_tags_view.xml',
        'views/estate_property_type_view.xml',
        'views/res_user_view.xml'
        
    ],
    'application': True,
}
