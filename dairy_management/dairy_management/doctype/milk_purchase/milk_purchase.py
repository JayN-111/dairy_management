# Copyright (c) 2026, jaynasit111@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class MilkPurchase(Document):
	def validate(self):
		self.calculate_total()

	def calculate_total(self):
		"""Total Price = Quantity × Rate per Liter"""
		if self.quantity and self.rate_per_liter:
			self.total_price = self.quantity * self.rate_per_liter

	def before_submit(self):
		if not self.quantity or not self.rate_per_liter:
			frappe.throw(
				"Please fill Quantity and Rate per Liter before submitting."
			)


@frappe.whitelist()
def check_purchase_receipt_exists(source_name):
	return frappe.db.exists('Purchase Receipt', {
		'remarks'  : source_name,
		'docstatus': 1
	})


@frappe.whitelist()
def make_purchase_receipt(source_name, target_doc=None):
	# Prevent duplicate
	if frappe.db.exists('Purchase Receipt', {
		'remarks'  : source_name,
		'docstatus': ['!=', 2]
	}):
		frappe.throw(
			f"A Purchase Receipt already exists for <b>{source_name}</b>."
		)

	def set_missing_values(source, target):
		target.supplier = source.supplier
		target.run_method('set_missing_values')

	doc = get_mapped_doc('Milk Purchase', source_name, {
		'Milk Purchase': {
			'doctype': 'Purchase Receipt',
			'field_map': {
				'supplier': 'supplier',
				'name'    : 'remarks'
			}
		}
	}, target_doc, set_missing_values)

	source    = frappe.get_doc('Milk Purchase', source_name)
	item_code = get_milk_item(source.milk_type)
	stock_uom = frappe.db.get_value('Item', item_code, 'stock_uom')
	warehouse = frappe.db.get_single_value(
		'Stock Settings', 'default_warehouse'
	)

	item_row                   = doc.append('items', {})
	item_row.item_code         = item_code
	item_row.item_name         = source.milk_type + ' Milk'
	item_row.qty               = source.quantity
	item_row.received_qty      = source.quantity
	item_row.accepted_qty      = source.quantity
	item_row.rate              = source.rate_per_liter
	item_row.price_list_rate   = source.rate_per_liter
	item_row.uom               = stock_uom
	item_row.stock_uom         = stock_uom
	item_row.conversion_factor = 1
	item_row.warehouse         = warehouse

	return doc


@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
	# Must have Purchase Receipt first
	pr = frappe.db.exists('Purchase Receipt', {
		'remarks'  : source_name,
		'docstatus': 1
	})

	if not pr:
		frappe.throw(
			"Cannot create Purchase Invoice without a submitted "
			"<b>Purchase Receipt</b>. "
			"Please create and submit the Purchase Receipt first."
		)

	# Prevent duplicate
	if frappe.db.exists('Purchase Invoice', {
		'remarks'  : source_name,
		'docstatus': ['!=', 2]
	}):
		frappe.throw(
			f"A Purchase Invoice already exists for <b>{source_name}</b>."
		)

	def set_missing_values(source, target):
		target.supplier = source.supplier
		target.run_method('set_missing_values')

	doc = get_mapped_doc('Milk Purchase', source_name, {
		'Milk Purchase': {
			'doctype': 'Purchase Invoice',
			'field_map': {
				'supplier': 'supplier',
				'name'    : 'remarks'
			}
		}
	}, target_doc, set_missing_values)

	source    = frappe.get_doc('Milk Purchase', source_name)
	item_code = get_milk_item(source.milk_type)
	stock_uom = frappe.db.get_value('Item', item_code, 'stock_uom')

	item_row                   = doc.append('items', {})
	item_row.item_code         = item_code
	item_row.item_name         = source.milk_type + ' Milk'
	item_row.qty               = source.quantity
	item_row.rate              = source.rate_per_liter
	item_row.price_list_rate   = source.rate_per_liter
	item_row.uom               = stock_uom
	item_row.stock_uom         = stock_uom
	item_row.conversion_factor = 1
	doc.update_stock           = 0

	return doc


def get_milk_item(milk_type):
	item_name = milk_type + ' Milk'
	item_code = frappe.db.get_value('Item', {'item_name': item_name}, 'name')

	if not item_code:
		frappe.throw(
			f"Item <b>{item_name}</b> not found in Item Master."
		)

	return item_code