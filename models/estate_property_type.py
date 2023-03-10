from odoo import models, fields

class PropertyType(models.Model):
    _name = 'estate_property_type'
    _description= 'Tipos de propiedades'
    _order = 'name desc'

    name = fields.Char(required=True)

    property_ids = fields.One2many(
        'estate_property',
        'property_type_id',
        string = 'Properties'
    )

    sequence = fields.Integer('Sequence')
    
    _sql_constraints= [
        ('unique_name', 
        'UNIQUE(name)', 
        'You can only have one type with same name'
        )
    ]

