from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

from dateutil.relativedelta import relativedelta

class PropertyOffer(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = 'estate_property_offer'
    _description= 'Ofertas de compra para las propiedades, hechas por clientes interesados'
    _order = 'price desc'
    _sql_constraints= [
        ('check_price', 
        'CHECK(price > 0)', 
        'The offer price must have values more than zero'
        )
    ]

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic

    price = fields.Float(string='Price')

    validity = fields.Integer(
        string='Validity(days)',
        default = 7
        )
    

    # Special

    state = fields.Selection(
        string = 'Status',
        copy = False,
        selection = [
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
        ]
    )

    # Relational

    partner_id = fields.Many2one(
        'res.partner', 
        string = 'Partner',
        required = True)
    
    property_id = fields.Many2one(
        'estate_property', 
        required = True)
    
    property_type_id = fields.Many2one(
        'estate_property_type',
        related='property_id.property_type_id',
        string = 'Property type',
        store = True
    )

    # Computed

    date_deadline = fields.Date(
        string = 'Deadline',
        compute = '_deadline_calculated',
        inverse = '_inverse_deadline_calculated',
        store = True
        )
    
    # ---------------------------------------- Compute methods ------------------------------------

    @api.depends('validity')
    def _deadline_calculated(self):
        for date in self:
            date.date_deadline = fields.Date.today() + relativedelta(days=date.validity)

    def _inverse_deadline_calculated(self):
        for value in self:  
            date = value.date_deadline - fields.Date.today()
            value.validity = int(date.days)


    # ------------------------------------------ CRUD Methods -------------------------------------
    
    @api.model
    def create(self, vals):
        if vals.get("property_id") and vals.get("price"):
            prop_price = self.env["estate_property"].browse(vals["property_id"])

            if prop_price.offer_ids:
                max_offer = max(prop_price.mapped("offer_ids.price"))
                if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                    raise UserError("The offer must be higher than %.2f" % max_offer)
            prop_price.state = "offer_received"
        return super().create(vals)
    

    # ---------------------------------------- Action Methods -------------------------------------

    def property_offer_accepted(self):
        if "accepted" in self.mapped("property_id.offer_ids.state"):
            raise UserError("An offer as already been accepted.")
        self.write(
            {
                "state": "accepted",
            }
        )
        return self.mapped("property_id").write(
            {
                "state": "offer_accepted",
                "selling_price": self.price,
                "buyer_id": self.partner_id.id,
            }
        )

    def property_offer_refused(self):
        return self.write(
            {
                "state": "refused",
            }
        )

    
            
    
    
    
    



            

