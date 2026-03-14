# Copyright (c) 2026, jaynasit111@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MemberManagement(Document):
	# pass

	def after_insert(self):
		if self.email:
			frappe.sendmail(
				recipients=[self.email],
				subject="Welcome to Dairy Management",
				message=f"""
					Hello {self.member_name},<br><br>

					Your registration is successful.<br><br>

					Member ID: {self.member_id}<br>
					Name: {self.member_name}<br>
					Mobile: {self.mobile}<br>
					City: {self.village}<br><br>

					Thank you for joining our Dairy System.
					"""
			)
