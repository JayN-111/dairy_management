# Copyright (c) 2026, jaynasit111@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now


class MilkTestSample(Document):
	def validate(self):
		self.set_grade()
		self.sync_status()

	def set_grade(self):
		if not self.fat or not self.milk_type:
			return

		if self.milk_type == 'Cow':
			if self.fat >= 4.5:        self.grade = 'A'
			elif self.fat >= 4.0:      self.grade = 'B'
			elif self.fat >= 3.0:      self.grade = 'C'
			else:                       self.grade = 'Rejected'

		elif self.milk_type == 'Buffalo':
			if self.fat >= 7.0:        self.grade = 'A'
			elif self.fat >= 6.0:      self.grade = 'B'
			elif self.fat >= 5.0:      self.grade = 'C'
			else:                       self.grade = 'Rejected'

	def sync_status(self):
		if self.workflow_state:
			self.status = self.workflow_state

	def before_submit(self):
		if self.workflow_state != 'Approved':
			frappe.throw(
				"Only <b>Approved</b> samples can be submitted."
			)

	def on_workflow_action(self, workflow_action):
		if workflow_action == 'Send For Approval':
			self.db_set('rejection_reason', None, update_modified=False)
			self.db_set('approver', None, update_modified=False)
			self.db_set('approved_on', None, update_modified=False)
			self.send_email_from_template(
				template_name='Milk Test Sample Approval Request',
				recipients=self.get_manager_emails()
			)

		elif workflow_action == 'Approve':
			# Prevent self approval
			if frappe.session.user == self.owner:
				frappe.throw(
					"You cannot approve a sample you created. "
					"A different Dairy Manager must approve it."
				)
			self.db_set('approver', frappe.session.user, update_modified=False)
			self.db_set('approved_on', now(), update_modified=False)
			self.send_email_from_template(
				template_name='Milk Test Sample Approved',
				recipients=[frappe.db.get_value('User', self.owner, 'email')]
			)

		elif workflow_action == 'Reject':
			self.db_set('approver', None, update_modified=False)
			self.db_set('approved_on', None, update_modified=False)
			self.send_email_from_template(
				template_name='Milk Test Sample Rejected',
				recipients=[frappe.db.get_value('User', self.owner, 'email')]
			)

		elif workflow_action == 'Resubmit':
			self.db_set('approver', None, update_modified=False)
			self.db_set('approved_on', None, update_modified=False)
			self.db_set('rejection_reason', None, update_modified=False)

	def get_manager_emails(self):
		managers = frappe.get_all(
			'Has Role',
			filters={
				'role': 'Dairy Manager',
				'parenttype': 'User'
			},
			fields=['parent']
		)
		return [
			m.parent for m in managers
			if m.parent != 'Administrator'
		]

	def send_email_from_template(self, template_name, recipients):
		if not recipients:
			return

		template = frappe.get_doc('Email Template', template_name)
		subject  = frappe.render_template(template.subject, {'doc': self})
		message  = frappe.render_template(template.response, {'doc': self})

		frappe.sendmail(
			recipients=recipients,
			subject=subject,
			message=message
		)