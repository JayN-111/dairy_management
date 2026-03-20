import frappe

@frappe.whitelist()
def get_summary(from_date=None, to_date=None):

	params = {}
	date_filter_pr = ""
	date_filter_dn = ""

	if from_date and to_date:
		date_filter_pr = "AND pr.posting_date BETWEEN %(from_date)s AND %(to_date)s"
		date_filter_dn = "AND dn.posting_date BETWEEN %(from_date)s AND %(to_date)s"
		params = {'from_date': from_date, 'to_date': to_date}
	elif from_date:
		date_filter_pr = "AND pr.posting_date >= %(from_date)s"
		date_filter_dn = "AND dn.posting_date >= %(from_date)s"
		params = {'from_date': from_date}
	elif to_date:
		date_filter_pr = "AND pr.posting_date <= %(to_date)s"
		date_filter_dn = "AND dn.posting_date <= %(to_date)s"
		params = {'to_date': to_date}

	# %% is needed to escape % in LIKE when using f-strings with frappe.db.sql
	buy = frappe.db.sql(f"""
		SELECT
			COALESCE(SUM(pri.qty), 0)    AS total_ltr,
			COALESCE(SUM(pri.amount), 0) AS total_price
		FROM `tabPurchase Receipt Item` pri
		JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
		WHERE pr.docstatus = 1
		{date_filter_pr}
		AND pri.item_code IN (
			SELECT name FROM `tabItem`
			WHERE item_name LIKE '%%Milk%%'
		)
	""", params, as_dict=True)

	buy = buy[0] if buy else {'total_ltr': 0, 'total_price': 0}

	sale = frappe.db.sql(f"""
		SELECT
			COALESCE(SUM(dni.qty), 0)    AS total_ltr,
			COALESCE(SUM(dni.amount), 0) AS total_price
		FROM `tabDelivery Note Item` dni
		JOIN `tabDelivery Note` dn ON dn.name = dni.parent
		WHERE dn.docstatus = 1
		{date_filter_dn}
		AND dni.item_code IN (
			SELECT name FROM `tabItem`
			WHERE item_name LIKE '%%Milk%%'
		)
	""", params, as_dict=True)

	sale = sale[0] if sale else {'total_ltr': 0, 'total_price': 0}

	pending_ltr = float(buy['total_ltr'] or 0) - float(sale['total_ltr'] or 0)

	return {
		'buy_ltr'    : float(buy['total_ltr']   or 0),
		'buy_price'  : float(buy['total_price'] or 0),
		'sale_ltr'   : float(sale['total_ltr']   or 0),
		'sale_price' : float(sale['total_price'] or 0),
		'pending_ltr': pending_ltr
	}