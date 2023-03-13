from odoo import models, fields

class PropertyType(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = 'estate_property_type'
    _description= 'Tipos de propiedades'
    _order = 'name desc'
    _sql_constraints= [
        ('unique_name', 
        'UNIQUE(name)', 
        'You can only have one type with same name'
        )
    ]

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic

    name = fields.Char(required=True)
    
    sequence = fields.Integer('Sequence')

    # Relational

    property_ids = fields.One2many(
        'estate_property',
        'property_type_id',
        string = 'Properties'
    )

    # Computed

    offer_ids = fields.Many2many(
        'estate_property_offer',
        string = 'Offers for each type',
        compute = '_compute_offer'
    )

    offer_count = fields.Integer(
        string = 'Offers count',
        compute ='_compute_offer'
    )

    # ---------------------------------------- Compute methods ------------------------------------    

    def _compute_offer(self):

        data = self.env["estate_property_offer"].read_group(
            [("property_id.state", "!=", "canceled"), ("property_type_id", "!=", False)],
            ["ids:array_agg(id)", "property_type_id"],
            ["property_type_id"],
        )
        mapped_count = {d["property_type_id"][0]: d["property_type_id_count"] for d in data}
        mapped_ids = {d["property_type_id"][0]: d["ids"] for d in data}
        for prop_type in self:
            prop_type.offer_count = mapped_count.get(prop_type.id, 0)
            prop_type.offer_ids = mapped_ids.get(prop_type.id, [])

    # ---------------------------------------- Action Methods -------------------------------------
    
    def action_view_offers(self):
        res = self.env.ref("estate.estate_property_offer_action").read()[0]
        res["domain"] = [("id", "in", self.offer_ids.ids)]
        return res
    
    

