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




			
