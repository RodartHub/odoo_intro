from odoo import models, fields

class PropertyType(models.Model):
    _name = 'estate_property_type'
    _description= 'Tipos de propiedades'

    name = fields.Char(required=True)

    _sql_constraints= [
        ('unique_name', 
        'UNIQUE(name)', 
        'You can only have one type with same name'
        )
    ]

