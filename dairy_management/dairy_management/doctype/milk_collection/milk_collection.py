# Copyright (c) 2026, jaynasit111@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class MilkCollection(Document):
	def validate(self):
		self.calculate_total_price()
		self.check_duplicate()

	def calculate_total_price(self):
		if self.quantity and self.fat and self.rate:
			self.total_price = self.quantity * self.fat * self.rate

	def check_duplicate(self):
		existing = frappe.db.exists('Milk Collection', {
			'customer': self.customer,
			'date'    : self.date,
			'shift'   : self.shift,
			'name'    : ('!=', self.name)
		})
		if existing:
			frappe.throw(
				f"Collection already exists for {self.customer} "
				f"on {self.date} - {self.shift}"
			)

	def validate_stock(self):
		"""Check warehouse stock before allowing delivery"""
		if not self.quantity or not self.milk_type:
			return

		item_code = get_milk_item(self.name)
		warehouse = frappe.db.get_single_value(
			'Stock Settings', 'default_warehouse'
		)

		stock_qty = frappe.db.get_value('Bin', {
			'item_code': item_code,
			'warehouse': warehouse
		}, 'actual_qty') or 0

		if stock_qty <= 0:
			frappe.throw(
				f"No stock available for <b>{self.milk_type} Milk</b> "
				f"in warehouse <b>{warehouse}</b>. "
				f"Please create a Milk Purchase from supplier first."
			)

		if self.quantity > stock_qty:
			frappe.throw(
				f"Cannot deliver <b>{self.quantity} Ltr</b>. "
				f"Only <b>{stock_qty} Ltr</b> available in warehouse."
			)


@frappe.whitelist()
def get_milk_rate(milk_type, fat):
	fat  = float(fat)
	rate = frappe.db.sql("""
		SELECT rate FROM `tabRate Master`
		WHERE milk_type = %(milk_type)s
		AND fat_from <= %(fat)s
		AND fat_to   >= %(fat)s
		ORDER BY creation DESC
		LIMIT 1
	""", {'milk_type': milk_type, 'fat': fat}, as_dict=True)

	if rate:
		return rate[0].rate
	frappe.throw(
		f"No rate found for {milk_type} milk at {fat}% fat. "
		f"Please configure it in Rate Master."
	)


@frappe.whitelist()
def check_delivery_note_exists(source_name):
	return frappe.db.exists('Delivery Note', {
		'remarks'  : source_name,
		'docstatus': 1
	})


@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None):
	source    = frappe.get_doc('Milk Collection', source_name)
	item_code = get_milk_item(source_name)
	warehouse = frappe.db.get_single_value(
		'Stock Settings', 'default_warehouse'
	)

	# Check stock before creating Delivery Note
	stock_qty = frappe.db.get_value('Bin', {
		'item_code': item_code,
		'warehouse': warehouse
	}, 'actual_qty') or 0

	if source.quantity > stock_qty:
		frappe.throw(
			f"Cannot deliver <b>{source.quantity} Ltr</b> of "
			f"{source.milk_type} Milk. "
			f"Only <b>{stock_qty} Ltr</b> in stock. "
			f"Please create a Milk Purchase first."
		)

	# Prevent duplicate
	if frappe.db.exists('Delivery Note', {
		'remarks'  : source_name,
		'docstatus': ['!=', 2]
	}):
		frappe.throw(
			f"A Delivery Note already exists for <b>{source_name}</b>."
		)

	def set_missing_values(source, target):
		target.run_method('set_missing_values')

	doc = get_mapped_doc('Milk Collection', source_name, {
		'Milk Collection': {
			'doctype': 'Delivery Note',
			'field_map': {
				'customer': 'customer',
				'name'    : 'remarks'
			}
		}
	}, target_doc, set_missing_values)

	stock_uom = frappe.db.get_value('Item', item_code, 'stock_uom')

	item_row                   = doc.append('items', {})
	item_row.item_code         = item_code
	item_row.item_name         = source.milk_type + ' Milk'
	item_row.qty               = source.quantity
	item_row.rate              = source.rate * source.fat
	item_row.uom               = stock_uom
	item_row.stock_uom         = stock_uom
	item_row.conversion_factor = 1
	item_row.warehouse         = warehouse

	return doc


@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None):
	# Must have Delivery Note first
	dn = frappe.db.exists('Delivery Note', {
		'remarks'  : source_name,
		'docstatus': 1
	})

	if not dn:
		frappe.throw(
			"Cannot create Sales Invoice without a submitted "
			"<b>Delivery Note</b>. "
			"Please create and submit the Delivery Note first."
		)

	# Prevent duplicate
	if frappe.db.exists('Sales Invoice', {
		'remarks'  : source_name,
		'docstatus': ['!=', 2]
	}):
		frappe.throw(
			f"A Sales Invoice already exists for <b>{source_name}</b>."
		)

	def set_missing_values(source, target):
		target.run_method('set_missing_values')

	doc = get_mapped_doc('Milk Collection', source_name, {
		'Milk Collection': {
			'doctype': 'Sales Invoice',
			'field_map': {
				'customer': 'customer',
				'name'    : 'remarks'
			}
		}
	}, target_doc, set_missing_values)

	source    = frappe.get_doc('Milk Collection', source_name)
	item_code = get_milk_item(source_name)
	stock_uom = frappe.db.get_value('Item', item_code, 'stock_uom')

	item_row                   = doc.append('items', {})
	item_row.item_code         = item_code
	item_row.item_name         = source.milk_type + ' Milk'
	item_row.qty               = source.quantity 
	item_row.rate              = source.rate * source.fat
	item_row.price_list_rate   = source.rate
	# item_row.amount            = source.total_price
	item_row.uom               = stock_uom
	item_row.stock_uom         = stock_uom
	item_row.conversion_factor = 1
	doc.update_stock           = 0

	return doc


def get_milk_item(source_name):
	milk_type = frappe.db.get_value('Milk Collection', source_name, 'milk_type')
	item_name = milk_type + ' Milk'
	item_code = frappe.db.get_value('Item', {'item_name': item_name}, 'name')

	if not item_code:
		frappe.throw(
			f"Item <b>{item_name}</b> not found in Item Master."
		)

	return item_code