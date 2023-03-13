from odoo import models, fields

class PropertyTag(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = 'estate_property_tag'
    _description= 'Etiquetas para las propiedades'
    _order = 'name desc'
    _sql_constraints= [
        ('unique_name', 
        'UNIQUE(name)', 
        'You can only have one tag with same name'
        )
    ]

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    
    name = fields.Char(required=True)
    
    color = fields.Integer(string='Color index')
    
    