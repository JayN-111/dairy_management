# Copyright (c) 2026, jaynasit111@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MilkCollection(Document):
	# pass

	def validate(self):
		existing = frappe.db.exists('Milk Collection', {
			'member': self.member,
			'date': self.date,
			'shift': self.shift,
			'name': ('!=', self.name)
		})
		if existing:
			frappe.throw(f"Collection already exists for {self.member} on {self.date} - {self.shift}")



@frappe.whitelist()
def get_milk_rate(milk_type, fat):
    fat = float(fat)

    rate = frappe.db.sql("""
        SELECT rate FROM `tabRate Master`
        WHERE milk_type = %(milk_type)s
        AND fat_from <= %(fat)s
        AND fat_to >= %(fat)s
        LIMIT 1
    """, {'milk_type': milk_type, 'fat': fat}, as_dict=True)

    if rate:
        return rate[0].rate
    else:
        frappe.throw(
            f"No active rate found for {milk_type} milk at {fat}% fat. "
            f"Please configure it in Rate Master."
        )