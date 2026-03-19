// Copyright (c) 2026, jaynasit111@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Milk Test Sample', {

	refresh(frm) {
		// Call directly — no frappe.after_ajax (causes timing issues)
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

		let fat = frm.doc.fat;
		let milk_type = frm.doc.milk_type;
		let grade;

		if (milk_type === 'Cow') {
			if (fat >= 4.5) grade = 'A';
			else if (fat >= 4.0) grade = 'B';
			else if (fat >= 3.0) grade = 'C';
			else grade = 'Rejected';

		} else if (milk_type === 'Buffalo') {
			if (fat >= 7.0) grade = 'A';
			else if (fat >= 6.0) grade = 'B';
			else if (fat >= 5.0) grade = 'C';
			else grade = 'Rejected';
		}

		frm.set_value('grade', grade);

		if (grade === 'Rejected') {
			frappe.show_alert({
				message: `⚠️ Fat % is below acceptable range for ${milk_type} milk. Grade set to Rejected.`,
				indicator: 'red'
			}, 5);
		}
	}
});


function set_approval_field_visibility(frm) {
	// ── Expand both sections (remove collapsible) ──
	frm.set_df_property('test_results_section_break_section', 'collapsible', 0);
	frm.set_df_property('approval_section_break_section', 'collapsible', 0);

	// ── Show all fields — no hidden, no read_only for any role ──
	let all_fields = ['approver', 'approved_on', 'remarks', 'rejection_reason', 'fat', 'water_'];
	all_fields.forEach(f => {
		frm.set_df_property(f, 'hidden', 0);
		frm.set_df_property(f, 'read_only', 0);
		frm.toggle_display(f, true);
	});

	frm.refresh_fields();
}


function set_status_color(frm) {
	const color_map = {
		'Draft': 'gray',
		'Sent for Approval': 'orange',
		'Approved': 'green',
		'Rejected': 'red'
	};

	const state = frm.doc.workflow_state || frm.doc.status || 'Draft';
	frm.page.set_indicator(state, color_map[state] || 'gray');
}