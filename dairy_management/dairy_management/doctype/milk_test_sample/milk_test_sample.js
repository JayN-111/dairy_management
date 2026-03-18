// Copyright (c) 2026, jaynasit111@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Milk Test Sample', {

	refresh(frm) {
		set_status_color(frm);
	},

	// Auto set grade when fat % is entered
	fat(frm) {
		if (!frm.doc.fat) return;

		let grade;
		if (frm.doc.fat >= 4.0)       grade = 'A';
		else if (frm.doc.fat >= 3.5)  grade = 'B';
		else if (frm.doc.fat >= 3.0)  grade = 'C';
		else                           grade = 'Rejected';

		frm.set_value('grade', grade);

		// Warn immediately if sample will be rejected
		if (grade === 'Rejected') {
			frappe.show_alert({
				message: `⚠️ Fat % is too low. This sample will be graded as Rejected.`,
				indicator: 'red'
			}, 5);
		}
	}
});


function set_status_color(frm) {
	const color_map = {
		'Draft':             'gray',
		'Sent for Approval': 'blue',
		'Approved':          'green',
		'Rejected':          'red'
	};

	const color = color_map[frm.doc.workflow_state] || 'gray';
	frm.page.set_indicator(frm.doc.workflow_state, color);
}