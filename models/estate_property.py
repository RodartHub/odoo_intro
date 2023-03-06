from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class PropertyEstate(models.Model):
    _name = 'estate_property'
    _description= 'Descripcion minima de este modelo.'

    name = fields.Char(default='Unknown',required=True)
    description= fields.Text()
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(
        string='Available From',
        default = lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False)
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(
        string='Bedrooms',
        default = 2)
    living_area = fields.Integer(string='Living area (m2)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (m2)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
        ('North', 'North'), 
        ('South', 'South'), 
        ('East', 'East'), 
        ('West', 'West')
        ]
    )

    @api.onchange('garden')
    def _onchange_garden_fields(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    last_seen = fields.Datetime(
        'Last Seen', 
        default = lambda self: fields.Datetime.now(), readonly=True
        )
    
    state = fields.Selection(
        default = 'New',
        string='Status',
        selection=[
        ('New', 'New'), 
        ('Offer received', 'Offer received'), 
        ('Offer Accepted', 'Offer Accepted'), 
        ('Sold', 'Sold'), 
        ('Canceled', 'Canceled')
        ]
    )
    
    active = fields.Boolean(
        string= "It's active?",
        active = False
    )

    property_type_id = fields.Many2one(
        'estate_property_type', 
        string='Type property', 
        ondelete='cascade')

    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer')

    salesman_id = fields.Many2one(
        'res.users',
        string = 'Salesman', 
        default = lambda self: self.env.user)
    
    property_tag_ids = fields.Many2many(
        'estate_property_tag', 
        string='Tags properties')

    offer_ids = fields.One2many(
        'estate_property_offer',
        'property_id', 
        string = 'offers')
    
    total_area = fields.Integer(
        string='Total area (m2)',
        compute='_total_area')

    @api.depends('living_area', 'garden_area')
    def _total_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area

    best_price = fields.Float(
        string = 'Best price',
        compute ='_best_price')
    
    @api.depends('offer_ids.price')
    def _best_price(self):
        for price in self:
            if price.best_price != 0:
                price.best_price = max(self.mapped('offer_ids.price'))
        





    

