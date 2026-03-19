// Copyright (c) 2026, jaynasit111@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Milk Purchase', {

	refresh(frm) {
		if (frm.doc.docstatus === 1) {

			// ── Always show both buttons ──

			frm.add_custom_button(__('Purchase Receipt'), () => {
				frappe.model.open_mapped_doc({
					method: 'dairy_management.dairy_management.doctype.milk_purchase.milk_purchase.make_purchase_receipt',
					frm: frm
				});
			}, __('Create'));

			frm.add_custom_button(__('Purchase Invoice'), () => {
				// Check if Purchase Receipt exists before opening
				frappe.call({
					method: 'dairy_management.dairy_management.doctype.milk_purchase.milk_purchase.check_purchase_receipt_exists',
					args: { source_name: frm.doc.name },
					callback(r) {
						if (!r.message) {
							frappe.msgprint({
								title    : 'Purchase Receipt Required',
								message  : 'Please create and submit a <b>Purchase Receipt</b> '
								         + 'before creating a Purchase Invoice.',
								indicator: 'orange'
							});
						} else {
							frappe.model.open_mapped_doc({
								method: 'dairy_management.dairy_management.doctype.milk_purchase.milk_purchase.make_purchase_invoice',
								frm: frm
							});
						}
					}
				});
			}, __('Create'));

			// Show headline based on PR status
			frappe.call({
				method: 'dairy_management.dairy_management.doctype.milk_purchase.milk_purchase.check_purchase_receipt_exists',
				args: { source_name: frm.doc.name },
				callback(r) {
					if (!r.message) {
						frm.dashboard.set_headline_alert(
							'<span style="color:orange">⚠️ Purchase Receipt not created yet. '
							+ 'Create Purchase Receipt before Purchase Invoice.</span>'
						);
					} else {
						frm.dashboard.set_headline_alert(
							'<span style="color:green">✅ Purchase Receipt submitted. '
							+ 'You can now create Purchase Invoice.</span>'
						);
					}
				}
			});
		}
	},

	quantity(frm)      { calculate_total(frm); },
	rate_per_liter(frm){ calculate_total(frm); }
});


function calculate_total(frm) {
	let total = (frm.doc.quantity || 0) * (frm.doc.rate_per_liter || 0);
	frm.set_value('total_price', total);
}