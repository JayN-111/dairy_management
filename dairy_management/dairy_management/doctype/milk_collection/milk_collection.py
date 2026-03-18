# Copyright (c) 2026, jaynasit111@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class MilkCollection(Document):
	# pass

	def validate(self):
		existing = frappe.db.exists('Milk Collection', {
			'name1': self.name1,
			'date': self.date,
			'shift': self.shift,
			'name': ['!=', self.name]
		})
		if existing:
			frappe.throw(f"Collection already exists for {self.name1} on {self.date} - {self.shift}")



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

@frappe.whitelist()
def make_purchase_receipt(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.run_method('set_missing_values')

	doc = get_mapped_doc('Milk Collection', source_name, {
		'Milk Collection': {
			'doctype': 'Purchase Receipt',
			'field_map': {
				'name': 'remarks',        # track source doc name in remarks
			}
		}
	}, target_doc, set_missing_values)

	stock_uom = frappe.db.get_value('Item', get_milk_item(source_name), 'stock_uom')

	# Manually add item row since Milk Collection is not a child-table based doc
	item_row = doc.append('items', {})
	item_row.item_code    = get_milk_item(source_name)  # fetch item code
	item_row.item_name    = frappe.db.get_value('Milk Collection', source_name, 'milk_type') + ' Milk'
	item_row.qty          = frappe.db.get_value('Milk Collection', source_name, 'quantity')
	item_row.rate         = frappe.db.get_value('Milk Collection', source_name, 'rate')
	item_row.uom          = stock_uom
	item_row.stock_uom    = stock_uom
	item_row.warehouse    = frappe.db.get_single_value('Stock Settings', 'default_warehouse')

	return doc


@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.run_method('set_missing_values')

	doc = get_mapped_doc('Milk Collection', source_name, {
		'Milk Collection': {
			'doctype': 'Purchase Invoice',
			'field_map': {
				'name': 'remarks',
			}
		}
	}, target_doc, set_missing_values)

	# Manually add item row
	source = frappe.get_doc('Milk Collection', source_name)
	item_code = get_milk_item(source_name)

	stock_uom = frappe.db.get_value('Item', item_code, 'stock_uom')

	item_row = doc.append('items', {})
	item_row.item_code    = item_code
	item_row.item_name    = source.milk_type + ' Milk'
	item_row.qty          = source.quantity
	item_row.rate         = source.rate
	item_row.uom          = stock_uom
	item_row.stock_uom    = stock_uom
	item_row.warehouse    = frappe.db.get_single_value('Stock Settings', 'default_warehouse')

	# Mark as non-stock purchase invoice if no warehouse setup
	doc.update_stock  = 0

	return doc


def get_milk_item(source_name):
    milk_type = frappe.db.get_value('Milk Collection', source_name, 'milk_type')

    item_name = milk_type + ' Milk'  # e.g. 'Cow Milk' or 'Buffalo Milk'

    # Search by item_name instead of item code
    item_code = frappe.db.get_value('Item', {'item_name': item_name}, 'name')

    if not item_code:
        frappe.throw(
            f"Item with name <b>{item_name}</b> not found in Item Master. "
            f"Please verify the Item Name spelling in Stock > Item."
        )

    return item_code