// Copyright (c) 2026, jaynasit111@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Milk Collection', {

	refresh(frm) {
		if (frm.doc.docstatus === 1) {

			frm.add_custom_button(__('Delivery Note'), () => {
				frappe.model.open_mapped_doc({
					method: 'dairy_management.dairy_management.doctype.milk_collection.milk_collection.make_delivery_note',
					frm: frm
				});
			}, __('Create'));

			frm.add_custom_button(__('Sales Invoice'), () => {
				// Check if Delivery Note exists before opening
				frappe.call({
					method: 'dairy_management.dairy_management.doctype.milk_collection.milk_collection.check_delivery_note_exists',
					args: { source_name: frm.doc.name },
					callback(r) {
						if (!r.message) {
							frappe.msgprint({
								title    : 'Delivery Note Required',
								message  : 'Please create and submit a <b>Delivery Note</b> '
								         + 'before creating a Sales Invoice.',
								indicator: 'orange'
							});
						} else {
							frappe.model.open_mapped_doc({
								method: 'dairy_management.dairy_management.doctype.milk_collection.milk_collection.make_sales_invoice',
								frm: frm
							});
						}
					}
				});
			}, __('Create'));

			// Show headline based on DN status
			frappe.call({
				method: 'dairy_management.dairy_management.doctype.milk_collection.milk_collection.check_delivery_note_exists',
				args: { source_name: frm.doc.name },
				callback(r) {
					if (!r.message) {
						frm.dashboard.set_headline_alert(
							'<span style="color:orange">⚠️ Delivery Note not created yet. '
							+ 'Create Delivery Note before Sales Invoice.</span>'
						);
					} else {
						frm.dashboard.set_headline_alert(
							'<span style="color:green">✅ Delivery Note submitted. '
							+ 'You can now create Sales Invoice.</span>'
						);
					}
				}
			});
		}
	},

	fat(frm)       { fetch_rate(frm); },
	milk_type(frm) { fetch_rate(frm); },
	quantity(frm)  { calculate_price(frm); },
	rate(frm)      { calculate_price(frm); }
});


function fetch_rate(frm) {
	if (!frm.doc.milk_type || !frm.doc.fat) return;

	frappe.call({
		method: 'dairy_management.dairy_management.doctype.milk_collection.milk_collection.get_milk_rate',
		args: {
			milk_type: frm.doc.milk_type,
			fat      : frm.doc.fat
		},
		callback(r) {
			if (r.message) {
				frm.set_value('rate', r.message);
				calculate_price(frm);
			}
		}
	});
}


function calculate_price(frm) {
	let price = (frm.doc.quantity || 0) * (frm.doc.fat || 0) * (frm.doc.rate || 0);
	frm.set_value('total_price', price);
}