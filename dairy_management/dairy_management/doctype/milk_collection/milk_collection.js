// Copyright (c) 2026, jaynasit111@gmail.com and contributors
// For license information, please see license.txt

<<<<<<< HEAD
frappe.ui.form.on("Milk Collection", {
	refresh(frm) {

	},
});
=======


frappe.ui.form.on("Milk Collection", {
    refresh(frm) {
        calc(frm);
    },
    quantity(frm) {
        calc(frm);
    },
    fat(frm) {
        calc(frm);
    },
    rate(frm) {
        calc(frm);
    }
});

function calc(frm) {
    if (frm.doc.quantity && frm.doc.fat && frm.doc.rate) {
        frm.doc.total_price = frm.doc.quantity * frm.doc.fat * frm.doc.rate;
        frm.refresh_field('total_price');
    }
}
>>>>>>> feature/member-management
