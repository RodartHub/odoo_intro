from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from dateutil.relativedelta import relativedelta

class PropertyEstate(models.Model):
    _name = 'estate_property'
    _description= 'Descripcion minima de este modelo.'
    _order = 'id desc'
    _sql_constraints= [
        ('check_expected_price', 
        'CHECK(expected_price > 0)', 
        'The expected price must have values more than zero'
        ),
        ('check_selling_price', 
        'CHECK(selling_price >= 0)', 
        'The selling price must have only positives values'
        ),
    ]

    name = fields.Char(
        string = 'Title',
        default='Unknown',
        required=True)
    
    description= fields.Text()

    postcode = fields.Char(string='Postcode')

    date_availability = fields.Date(
        string='Available From',
        default = lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False)
    
    expected_price = fields.Float(string='Expected Price')

    selling_price = fields.Float(
        compute='_change_selling_price',
        copy=False, 
        readonly=True
        )
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

    last_seen = fields.Datetime(
        'Last Seen', 
        default = lambda self: fields.Datetime.now(), 
        readonly=True
        )
    
    state = fields.Selection(
        default = 'New',
        string='Status',
        required = True,
        selection=[
        ('new', 'New'), 
        ('offer_received', 'Offer Received'), 
        ('offer_accepted', 'Offer Accepted'), 
        ('sold', 'Sold'), 
        ('canceled', 'Canceled')
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
        string='Buyer',
        readonly=True,
        copy=False)
    
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
        string = 'O ffers')
    
    total_area = fields.Integer(
        string='Total area (m2)',
        compute='_total_area')
    
    best_price = fields.Float(
        string = 'Best price',
        compute ='_best_price'
        )

    @api.onchange('garden')
    def _onchange_garden_fields(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

            
    def property_status_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties cannot be sold.")
        return self.write({"state": "sold"})

    def property_status_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled.")
        return self.write({"state": "canceled"})
            
    @api.depends('living_area', 'garden_area')
    def _total_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area

    
    @api.depends('offer_ids.price')
    def _best_price(self):
        self.best_price = 0
        for price in self:
            price_list = self.mapped('offer_ids.price')

            if len(price_list) > 0:
                price.best_price = max(price_list)


    @api.depends('offer_ids')
    def _change_selling_price(self):
        self.selling_price = 0
        self.buyer_id = ''

        for state in self.offer_ids:
            if state.state == 'accepted':
                self.selling_price = state.price
                self.buyer_id = state.partner_id
                
    @api.constrains('selling_price','expected_price')
    def _compare_prices(self):
        for price in self:
            if (
                not float_is_zero(price.selling_price, precision_rounding=0.01)
                and float_compare(price.selling_price, price.expected_price * 0.9, precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90 porc of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )

    @api.ondelete(at_uninstall = False) 
    def unlink(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise UserError("Only new and canceled properties can be deleted.")
        return super().unlink()






    