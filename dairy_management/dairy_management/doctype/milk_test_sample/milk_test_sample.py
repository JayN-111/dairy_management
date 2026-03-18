# Copyright (c) 2026, jaynasit111@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MilkTestSample(Document):
	def validate(self):
		self.set_grade()

	def set_grade(self):
		"""Auto set grade based on fat %"""
		if not self.fat:
			return

		if self.fat >= 4.0:
			self.grade = 'A'
		elif self.fat >= 3.5:
			self.grade = 'B'
		elif self.fat >= 3.0:
			self.grade = 'C'
		else:
			self.grade = 'Rejected'

	def on_submit(self):
		if self.workflow_state != 'Approved':
			frappe.throw(
				"Only <b>Approved</b> samples can be submitted."
			)

	def on_update_after_submit(self):
		pass

	def after_workflow_action(self, workflow_action):
		"""Triggered automatically on every workflow transition"""

		if workflow_action == 'Send for Approval':
			self.notify_approvers()

		elif workflow_action == 'Approve':
			self.notify_submitter('Approved')

		elif workflow_action == 'Reject':
			self.notify_submitter('Rejected')

	def notify_approvers(self):
		"""Email all users with Dairy Manager role when sent for approval"""
		managers = frappe.get_all(
			'Has Role',
			filters={'role': 'Dairy Manager', 'parenttype': 'User'},
			fields=['parent']
		)

		emails = [m.parent for m in managers if m.parent != 'Administrator']

		if emails:
			frappe.sendmail(
				recipients=emails,
				subject=f"Milk Test Sample Approval Required — {self.name}",
				message=f"""
					<p>A milk test sample requires your approval.</p>
					<table border="1" cellpadding="8"
					style="border-collapse:collapse; font-size:13px;">
						<tr><td><b>Sample ID</b></td><td>{self.name}</td></tr>
						<tr><td><b>Member</b></td><td>{self.member}</td></tr>
						<tr><td><b>Date</b></td><td>{self.collection_date}</td></tr>
						<tr><td><b>Milk Type</b></td><td>{self.milk_type}</td></tr>
						<tr><td><b>Fat %</b></td><td>{self.fat}</td></tr>
						<tr><td><b>Grade</b></td><td>{self.grade}</td></tr>
					</table>
					<br>
					<a href="/app/milk-test-sample/{self.name}">
						Click here to Review & Approve
					</a>
				"""
			)

	def notify_submitter(self, action):
		"""Notify the person who created the sample about approval/rejection"""
		creator_email = frappe.db.get_value(
			'User', self.owner, 'email'
		)

		color   = 'green' if action == 'Approved' else 'red'
		subject = f"Milk Test Sample {action} — {self.name}"

		if creator_email:
			frappe.sendmail(
				recipients=[creator_email],
				subject=subject,
				message=f"""
					<p>Your milk test sample <b>{self.name}</b>
					has been <b style="color:{color}">{action}</b>.</p>
					<table border="1" cellpadding="8"
					style="border-collapse:collapse; font-size:13px;">
						<tr><td><b>Member</b></td><td>{self.member}</td></tr>
						<tr><td><b>Grade</b></td><td>{self.grade}</td></tr>
						<tr><td><b>Remarks</b></td><td>{self.remarks or '—'}</td></tr>
					</table>
					<br>
					<a href="/app/milk-test-sample/{self.name}">View Sample</a>
				"""
			)