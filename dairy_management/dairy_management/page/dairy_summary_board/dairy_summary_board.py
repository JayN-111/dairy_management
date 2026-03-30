import frappe

@frappe.whitelist()
def get_summary(from_date=None, to_date=None):

	if not from_date or not to_date:
		return {
			'buy_ltr'    : 0,
			'buy_price'  : 0,
			'sale_ltr'   : 0,
			'sale_price' : 0,
			'pending_ltr': 0,
			'stock_details': []
		}

	params = {'from_date': from_date, 'to_date': to_date}

	buy = frappe.db.sql("""
		SELECT
			COALESCE(SUM(pri.qty), 0) AS total_ltr,
			COALESCE(SUM(pri.amount), 0) AS total_price
		FROM `tabPurchase Receipt Item` pri
		JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
		WHERE pr.docstatus = 1
		AND pr.posting_date BETWEEN %(from_date)s AND %(to_date)s
		AND pri.item_code IN ('CM-P-001', 'BM-P-001')
	""", params, as_dict=True)

	buy = buy[0] if buy else {'total_ltr': 0, 'total_price': 0}


	sale = frappe.db.sql("""
		SELECT
			COALESCE(SUM(dni.qty), 0) AS total_ltr,
			COALESCE(SUM(dni.amount), 0) AS total_price
		FROM `tabDelivery Note Item` dni
		JOIN `tabDelivery Note` dn ON dn.name = dni.parent
		WHERE dn.docstatus = 1
		AND dn.posting_date BETWEEN %(from_date)s AND %(to_date)s
		AND dni.item_code IN ('CM-P-001', 'BM-P-001')
	""", params, as_dict=True)

	sale = sale[0] if sale else {'total_ltr': 0, 'total_price': 0}


	buy_ltr = float(buy['total_ltr'] or 0)
	sale_ltr = float(sale['total_ltr'] or 0)

	pending_ltr = buy_ltr - sale_ltr
	low_stock = 50

	return {
		'has_data'    : True,
		'buy_ltr'     : buy_ltr,
		'buy_price'   : float(buy['total_price'] or 0),
		'sale_ltr'    : sale_ltr,
		'sale_price'  : float(sale['total_price'] or 0),
		'pending_ltr' : pending_ltr,
		'stock_details': [],
		'is_low_stock': pending_ltr < low_stock,
	}