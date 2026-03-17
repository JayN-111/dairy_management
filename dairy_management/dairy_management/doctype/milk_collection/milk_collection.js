// Copyright (c) 2026, jaynasit111@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Milk Collection', {

	refresh(frm) {
		// Only show Create buttons on submitted documents
		if (frm.doc.docstatus === 1) {

			frm.add_custom_button(__('Purchase Receipt'), () => {
				frappe.model.open_mapped_doc({
					method: 'dairy_management.dairy_management.doctype.milk_collection.milk_collection.make_purchase_receipt',
					frm: frm
				});
			}, __('Create'));

			frm.add_custom_button(__('Purchase Invoice'), () => {
				frappe.model.open_mapped_doc({
					method: 'dairy_management.dairy_management.doctype.milk_collection.milk_collection.make_purchase_invoice',
					frm: frm
				});
			}, __('Create'));
		}
	},

	// Trigger fetch when fat or milk type changes
	fat(frm)       { fetch_rate(frm); },
	milk_type(frm) { fetch_rate(frm); },

	// Recalculate total when quantity or rate changes
	quantity(frm)  { calculate_price(frm); },
	rate(frm)      { calculate_price(frm); }
});

function fetch_rate(frm) {
	if (!frm.doc.milk_type || !frm.doc.fat) return;

	frappe.call({
		method: 'dairy_management.dairy_management.doctype.milk_collection.milk_collection.get_milk_rate',
		args: {
			milk_type: frm.doc.milk_type,
			fat: frm.doc.fat
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