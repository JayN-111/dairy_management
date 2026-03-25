# Copyright (c) 2026, jaynasit111@gmail.com and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	filters = filters or {}
	report_type = filters.get('report_type', 'Buy History')

	if report_type == 'Buy History':
		return get_buy_history(filters)

	elif report_type == 'Sale History':
		return get_sale_history(filters)

	elif report_type == 'Summary':
		return get_summary(filters)

	return [], []


def get_buy_history(filters):
	columns = [
		{'label': 'Date',          'fieldname': 'date',
		 'fieldtype': 'Date',      'width': 110},
		{'label': 'Purchase Receipt', 'fieldname': 'receipt',
		 'fieldtype': 'Link',      'options': 'Purchase Receipt', 'width': 160},
		{'label': 'Supplier',      'fieldname': 'supplier',
		 'fieldtype': 'Link',      'options': 'Supplier', 'width': 150},
		{'label': 'Milk Type',     'fieldname': 'milk_type',
		 'fieldtype': 'Data',      'width': 100},
		{'label': 'Quantity (Ltr)','fieldname': 'quantity',
		 'fieldtype': 'Float',     'width': 120},
		{'label': 'Rate (₹/Ltr)', 'fieldname': 'rate',
		 'fieldtype': 'Currency',  'width': 120},
		{'label': 'Amount (₹)',   'fieldname': 'amount',
		 'fieldtype': 'Currency',  'width': 130},
	]

	conditions, params = build_buy_conditions(filters)

	data = frappe.db.sql(f"""
		SELECT
			pr.posting_date  AS date,
			pr.name          AS receipt,
			pr.supplier      AS supplier,
			pri.item_name    AS milk_type,
			pri.qty          AS quantity,
			pri.rate         AS rate,
			pri.amount       AS amount
		FROM `tabPurchase Receipt Item` pri
		JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
		WHERE pr.docstatus = 1
		AND pri.item_code IN (
			SELECT name FROM `tabItem`
			WHERE item_name LIKE '%%Milk%%'
		)
		{conditions}
		ORDER BY pr.posting_date DESC
	""", params, as_dict=True)

	# Summary row at bottom
	if data:
		total_qty    = sum(r.quantity or 0 for r in data)
		total_rate   = sum(r.rate     or 0 for r in data)
		total_amount = sum(r.amount   or 0 for r in data)

		data.append({
			'date'     : '',
			'receipt'  : '',
			'supplier' : 'Total',
			'milk_type': '',
			'quantity' : total_qty,
			'rate'     : total_rate,
			'amount'   : total_amount,
			'bold'     : 1
		})

	return columns, data


def get_sale_history(filters):
	columns = [
		{'label': 'Date',         'fieldname': 'date',
		 'fieldtype': 'Date',     'width': 110},
		{'label': 'Delivery Note','fieldname': 'delivery_note',
		 'fieldtype': 'Link',     'options': 'Delivery Note', 'width': 160},
		{'label': 'Customer',     'fieldname': 'customer',
		 'fieldtype': 'Link',     'options': 'Customer', 'width': 150},
		{'label': 'Milk Type',    'fieldname': 'milk_type',
		 'fieldtype': 'Data',     'width': 100},
		# {'label': 'Shift',        'fieldname': 'shift',
		#  'fieldtype': 'Data',     'width': 150},
		{'label': 'Quantity (Ltr)','fieldname': 'quantity',
		 'fieldtype': 'Float',    'width': 120},
		{'label': 'Rate (₹/Ltr)', 'fieldname': 'rate',
		 'fieldtype': 'Currency', 'width': 120},
		{'label': 'Amount (₹)',  'fieldname': 'amount',
		 'fieldtype': 'Currency', 'width': 130},
	]

	conditions, params = build_sale_conditions(filters)

	data = frappe.db.sql(f"""
		SELECT
			dn.posting_date  AS date,
			dn.name          AS delivery_note,
			dn.customer      AS customer,
			dni.item_name    AS milk_type,
			# dn.remarks       AS shift,
			dni.qty          AS quantity,
			dni.rate         AS rate,
			dni.amount       AS amount
		FROM `tabDelivery Note Item` dni
		JOIN `tabDelivery Note` dn ON dn.name = dni.parent
		WHERE dn.docstatus = 1
		AND dni.item_code IN (
			SELECT name FROM `tabItem`
			WHERE item_name LIKE '%%Milk%%'
		)
		{conditions}
		ORDER BY dn.posting_date DESC
	""", params, as_dict=True)

	# Summary row
	if data:
		total_qty    = sum(r.quantity or 0 for r in data)
		total_rate   = sum(r.rate     or 0 for r in data)
		total_amount = sum(r.amount   or 0 for r in data)

		data.append({
			'date'         : '',
			'delivery_note': '',
			'customer'     : 'Total',
			'milk_type'    : '',
			'shift'        : '',
			'quantity'     : total_qty,
			'rate'         : total_rate,
			'amount'       : total_amount,
			'bold'         : 1
		})

	return columns, data


def get_summary(filters):
	columns = [
		{'label': 'Milk Type',       'fieldname': 'milk_type',
		 'fieldtype': 'Data',        'width': 120},
		{'label': 'Buy Qty (Ltr)',   'fieldname': 'buy_qty',
		 'fieldtype': 'Float',       'width': 130},
		{'label': 'Buy Amount (₹)', 'fieldname': 'buy_amount',
		 'fieldtype': 'Currency',    'width': 140},
		{'label': 'Sale Qty (Ltr)',  'fieldname': 'sale_qty',
		 'fieldtype': 'Float',       'width': 130},
		{'label': 'Sale Amount (₹)','fieldname': 'sale_amount',
		 'fieldtype': 'Currency',    'width': 140},
		{'label': 'Pending Stock (Ltr)', 'fieldname': 'pending_qty',
		 'fieldtype': 'Float',       'width': 150},
	]

	buy_cond,  buy_params  = build_buy_conditions(filters)
	sale_cond, sale_params = build_sale_conditions(filters)

	buy_data = frappe.db.sql(f"""
		SELECT
			pri.item_name  AS milk_type,
			SUM(pri.qty)   AS qty,
			SUM(pri.amount)AS amount
		FROM `tabPurchase Receipt Item` pri
		JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
		WHERE pr.docstatus = 1
		AND pri.item_code IN (
			SELECT name FROM `tabItem`
			WHERE item_name LIKE '%%Milk%%'
		)
		{buy_cond}
		GROUP BY pri.item_name
	""", buy_params, as_dict=True)

	sale_data = frappe.db.sql(f"""
		SELECT
			dni.item_name  AS milk_type,
			SUM(dni.qty)   AS qty,
			SUM(dni.amount)AS amount
		FROM `tabDelivery Note Item` dni
		JOIN `tabDelivery Note` dn ON dn.name = dni.parent
		WHERE dn.docstatus = 1
		AND dni.item_code IN (
			SELECT name FROM `tabItem`
			WHERE item_name LIKE '%%Milk%%'
		)
		{sale_cond}
		GROUP BY dni.item_name
	""", sale_params, as_dict=True)

	bin_data = frappe.db.sql("""
		SELECT
			i.item_name  AS milk_type,
			SUM(b.actual_qty) AS actual_qty
		FROM `tabBin` b
		JOIN `tabItem` i ON i.name = b.item_code
		WHERE i.item_name LIKE '%%Milk%%'
		GROUP BY i.item_name
	""", as_dict=True)

	bin_map  = {r.milk_type: float(r.actual_qty or 0) for r in bin_data}
	buy_map  = {r.milk_type: r for r in buy_data}
	sale_map = {r.milk_type: r for r in sale_data}

	milk_types = set(
		list(buy_map.keys()) +
		list(sale_map.keys()) +
		list(bin_map.keys())
	)

	data             = []
	total_buy_qty    = 0
	total_buy_amount = 0
	total_sale_qty   = 0
	total_sale_amount= 0
	total_pending    = 0

	for mt in sorted(milk_types):
		buy_qty    = float(buy_map.get(mt,  {}).get('qty',    0) or 0)
		buy_amount = float(buy_map.get(mt,  {}).get('amount', 0) or 0)
		sale_qty   = float(sale_map.get(mt, {}).get('qty',    0) or 0)
		sale_amount= float(sale_map.get(mt, {}).get('amount', 0) or 0)

		pending = bin_map.get(mt, 0)

		data.append({
			'milk_type'  : mt,
			'buy_qty'    : buy_qty,
			'buy_amount' : buy_amount,
			'sale_qty'   : sale_qty,
			'sale_amount': sale_amount,
			'pending_qty': pending
		})

		total_buy_qty     += buy_qty
		total_buy_amount  += buy_amount
		total_sale_qty    += sale_qty
		total_sale_amount += sale_amount
		total_pending     += pending

	data.append({
		'milk_type'  : 'Total',
		'buy_qty'    : total_buy_qty,
		'buy_amount' : total_buy_amount,
		'sale_qty'   : total_sale_qty,
		'sale_amount': total_sale_amount,
		'pending_qty': total_pending,
		'bold'       : 1
	})

	return columns, data



def build_buy_conditions(filters):
	conditions = ""
	params     = {}

	if filters.get('from_date') and filters.get('to_date'):
		conditions += " AND pr.posting_date BETWEEN %(from_date)s AND %(to_date)s"
		params['from_date'] = filters['from_date']
		params['to_date']   = filters['to_date']
	elif filters.get('from_date'):
		conditions += " AND pr.posting_date >= %(from_date)s"
		params['from_date'] = filters['from_date']
	elif filters.get('to_date'):
		conditions += " AND pr.posting_date <= %(to_date)s"
		params['to_date'] = filters['to_date']

	if filters.get('supplier'):
		conditions += " AND pr.supplier = %(supplier)s"
		params['supplier'] = filters['supplier']

	if filters.get('milk_type'):
		conditions += " AND pri.item_name LIKE %(milk_type)s"
		params['milk_type'] = f"%{filters['milk_type']}%"

	return conditions, params


def build_sale_conditions(filters):
	conditions = ""
	params     = {}

	if filters.get('from_date') and filters.get('to_date'):
		conditions += " AND dn.posting_date BETWEEN %(from_date)s AND %(to_date)s"
		params['from_date'] = filters['from_date']
		params['to_date']   = filters['to_date']
	elif filters.get('from_date'):
		conditions += " AND dn.posting_date >= %(from_date)s"
		params['from_date'] = filters['from_date']
	elif filters.get('to_date'):
		conditions += " AND dn.posting_date <= %(to_date)s"
		params['to_date'] = filters['to_date']

	if filters.get('customer'):
		conditions += " AND dn.customer = %(customer)s"
		params['customer'] = filters['customer']

	if filters.get('milk_type'):
		conditions += " AND dni.item_name LIKE %(milk_type)s"
		params['milk_type'] = f"%{filters['milk_type']}%"

	return conditions, params