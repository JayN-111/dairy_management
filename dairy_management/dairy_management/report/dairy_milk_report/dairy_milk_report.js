// Copyright (c) 2026, jaynasit111@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports['Dairy Milk Report'] = {
	filters: [
		{
			fieldname : 'report_type',
			label     : 'Report Type',
			fieldtype : 'Select',
			options   : 'Buy History\nSale History\nSummary',
			default   : 'Buy History',
			reqd      : 1,
			on_change() {
				toggle_filters(
					frappe.query_report.get_filter_value('report_type')
				);
				frappe.query_report.refresh();
			}
		},
		{
			fieldname : 'from_date',
			label     : 'From Date',
			fieldtype : 'Date',
			default   : frappe.datetime.month_start()
		},
		{
			fieldname : 'to_date',
			label     : 'To Date',
			fieldtype : 'Date',
			default   : frappe.datetime.get_today()
		},
		{
			fieldname : 'supplier',
			label     : 'Supplier',
			fieldtype : 'Link',
			options   : 'Supplier'
		},
		{
			fieldname : 'customer',
			label     : 'Customer',
			fieldtype : 'Link',
			options   : 'Customer'
		},
		{
			fieldname : 'milk_type',
			label     : 'Milk Type',
			fieldtype : 'Select',
			options   : '\nCow\nBuffalo'
		},
		{
			fieldname : 'shift',
			label     : 'Shift',
			fieldtype : 'Select',
			options   : '\nMorning\nEvening'
		}
	],

	onload(report) {
		// Set initial filter visibility
		toggle_filters('Buy History');
	}
};


function toggle_filters(report_type) {
	// Supplier — only for Buy History
	frappe.query_report.toggle_filter_display(
		'supplier',
		report_type !== 'Buy History'
	);

	// Customer — only for Sale History
	frappe.query_report.toggle_filter_display(
		'customer',
		report_type !== 'Sale History'
	);

	// Shift — not relevant for Summary
	frappe.query_report.toggle_filter_display(
		'shift',
		report_type === 'Summary'
	);
}