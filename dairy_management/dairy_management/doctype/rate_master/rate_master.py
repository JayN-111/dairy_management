# Copyright (c) 2026, jaynasit111@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RateMaster(Document):
	# pass
	def validate(self):
		self.validate_fat_range()

	def validate_fat_range(self):
		if self.fat_from >= self.fat_to:
			frappe.throw("Fat From must be less than Fat To")

		# Check for overlapping ranges for same milk type
		overlapping = frappe.db.sql("""
			SELECT name FROM `tabRate Master`
			WHERE milk_type = %(milk_type)s
			AND name != %(name)s
			AND (
				%(fat_from)s < fat_to AND %(fat_to)s > fat_from
			)
		""", {
			'milk_type': self.milk_type,
			'fat_from': self.fat_from,
			'fat_to': self.fat_to,
			'name': self.name or ''
		})

		if overlapping:
			frappe.throw(
				f"Fat range {self.fat_from}–{self.fat_to} overlaps with an "
				f"existing rate for {self.milk_type}. "
				f"Conflicting record: {overlapping[0][0]}"
			)
