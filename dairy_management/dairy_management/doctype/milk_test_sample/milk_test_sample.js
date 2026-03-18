// Copyright (c) 2026, jaynasit111@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Milk Test Sample', {

	refresh(frm) {
		set_status_color(frm);
		set_approval_field_visibility(frm);
	},

	milk_type(frm) {
		if (frm.doc.fat) {
			frm.trigger('fat');
		}
	},

	fat(frm) {
		if (!frm.doc.fat || !frm.doc.milk_type) return;

		let fat       = frm.doc.fat;
		let milk_type = frm.doc.milk_type;
		let grade;

		if (milk_type === 'Cow') {
			if (fat >= 4.5)       grade = 'A';
			else if (fat >= 4.0)  grade = 'B';
			else if (fat >= 3.0)  grade = 'C';
			else                   grade = 'Rejected';

		} else if (milk_type === 'Buffalo') {
			if (fat >= 7.0)       grade = 'A';
			else if (fat >= 6.0)  grade = 'B';
			else if (fat >= 5.0)  grade = 'C';
			else                   grade = 'Rejected';
		}

		frm.set_value('grade', grade);

		if (grade === 'Rejected') {
			frappe.show_alert({
				message: `⚠️ Fat % is below acceptable range for 
				          ${milk_type} milk. Grade set to Rejected.`,
				indicator: 'red'
			}, 5);
		}
	}
});


function set_approval_field_visibility(frm) {
	let state      = frm.doc.workflow_state;
	let is_manager = frappe.user.has_role('Dairy Manager');

	frm.set_df_property('status', 'read_only', 1);
	frm.set_df_property('approver', 'read_only', 1);
	frm.set_df_property('approved_on', 'read_only', 1);

	// Remarks editable only by Dairy Manager when Sent for Approval
	frm.set_df_property('remarks', 'read_only',
		(state === 'Sent for Approval' && is_manager) ? 0 : 1
	);

	// Rejection Reason visible only when Rejected
	frm.set_df_property('rejection_reason', 'hidden',
		state === 'Rejected' ? 0 : 1
	);

	frm.set_df_property('rejection_reason', 'read_only',
		(state === 'Sent for Approval' && is_manager) ? 0 : 1
	);
}


function set_status_color(frm) {
	const color_map = {
		'Draft':             'gray',
		'Sent for Approval': 'orange',
		'Approved':          'green',
		'Rejected':          'red'
	};

	const state = frm.doc.workflow_state || frm.doc.status || 'Draft';
	frm.page.set_indicator(state, color_map[state] || 'gray');
}