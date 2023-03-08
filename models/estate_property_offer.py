from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

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

    validity = fields.Integer(
        string='Validity(days)',
        default = 7
        )

    date_deadline = fields.Date(
        string = 'Deadline',
        compute = '_deadline_calculated',
        inverse = '_inverse_deadline_calculated',
        store = True
        )
    
    _sql_constraints= [
        ('check_price', 
        'CHECK(price > 0)', 
        'The offer price must have values more than zero'
        )
    ]

    def property_offer_accepted(self):
        for record in self:
            record.state = 'Accepted'
            return True

    def property_offer_refused(self):
        for record in self:
            record.state = 'Refused'
            return True

    @api.depends('validity')
    def _deadline_calculated(self):
        for date in self:
            date.date_deadline = fields.Date.today() + relativedelta(days=date.validity)
            
    
    def _inverse_deadline_calculated(self):
        for value in self:  
            date = value.date_deadline - fields.Date.today()
            value.validity = int(date.days)
            

            

