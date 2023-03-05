from odoo import models, fields

class PropertyOffer(models.Model):
    _name = 'estate_property_offer'
    _description= 'Ofertas de compra para las propiedades, hechas por clientes interesados'

    price = fields.Float(string='Price')
    state = fields.Selection(
        string = 'Status',
        copy = False,
        selection = [
        ('Accepted', 'Accepted'),
        ('Refused', 'Refused')
        ]
    )

    partner_id = fields.Many2one(
        'res.partner', 
        string = 'Partner',
        required = True)
    
    property_id = fields.Many2one(
        'estate_property', 
        required = True)
    
    