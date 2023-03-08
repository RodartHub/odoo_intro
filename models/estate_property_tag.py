from odoo import models, fields

class PropertyTag(models.Model):
    _name = 'estate_property_tag'
    _description= 'Etiquetas para las propiedades'

    name = fields.Char(required=True)

    _sql_constraints= [
        ('unique_name', 
        'UNIQUE(name)', 
        'You can only have one tag with same name'
        )
    ]