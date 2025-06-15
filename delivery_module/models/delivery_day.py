from odoo import models, fields, api

class DeliveryDay(models.Model):
    _name = 'delivery.day'
    _description = 'Teslimat Günü'
    _order = 'sequence, name'

    name = fields.Char(string='Gün Adı', required=True)
    code = fields.Char(string='Gün Kodu', required=True)
    sequence = fields.Integer(string='Sıra', default=10)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Şirket', required=True, default=lambda self: self.env.company)

    _sql_constraints = [
        ('code_uniq', 'unique(code, company_id)', 'Gün kodu şirket bazında benzersiz olmalıdır!')
    ] 