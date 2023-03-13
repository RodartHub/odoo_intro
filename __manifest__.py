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
        'views/estate_property_views.xml', 
        'views/estate_new_views.xml',
        'views/property_types.xml',
        'views/property_type_view.xml',
        'views/property_tags.xml',
        'views/property_tags_view.xml',
        'views/property_offer_view.xml',
        'views/res_user_views.xml',
        'views/estate_menu.xml'
        
    ],
    'application': True,
}
