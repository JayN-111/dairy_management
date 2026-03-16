// Copyright (c) 2026, jaynasit111@gmail.com and contributors
// For license information, please see license.txt



frappe.ui.form.on('Milk Collection', {

    // Trigger fetch when fat or milk type changes
    fat(frm)       { fetch_rate(frm); },
    milk_type(frm) { fetch_rate(frm); },
    quantity(frm)  { calculate_price(frm); },

    // Recalculate total when rate changes
    rate(frm)      { calculate_price(frm); }
});

function fetch_rate(frm) {
    // Only fetch if both fields are filled
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
                calculate_price(frm);  // recalculate total immediately
            }
        }
    });
}

function calculate_price(frm) {
    let price = (frm.doc.quantity || 0) * (frm.doc.fat || 0) * (frm.doc.rate || 0);
    frm.set_value('total_price', price);
}
