from odoo import models, fields, api

class DeliveryDay(models.Model):
    _name = 'delivery.day'
    _description = 'Teslimat Günü'

    name = fields.Char(string='Gün Adı', required=True)
    code = fields.Char(string='Gün Kodu', required=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Şirket', required=True, default=lambda self: self.env.company)

    _sql_constraints = [
        ('code_uniq', 'unique(code, company_id)', 'Gün kodu şirket bazında benzersiz olmalıdır!')
    ] 