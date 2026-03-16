// Copyright (c) 2026, jaynasit111@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rate Master", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__('Update Rate'), () => {

				// Fetch current saved rate from DB as "previous rate"
				frappe.db.get_value('Rate Master', frm.doc.name, 'rate')
					.then(r => {
						let previous_rate = r.message.rate;

						let dialog = new frappe.ui.Dialog({
							title: __('Update Rate'),
							fields: [
								{
									fieldtype: 'HTML',
									options: `
										<div style="margin-bottom:15px; padding:10px; 
										background:#f5f5f5; border-radius:6px; font-size:13px;">
											<b>Milk Type:</b> ${frm.doc.milk_type} &nbsp;|&nbsp;
											<b>Fat Range:</b> ${frm.doc.fat_from} – ${frm.doc.fat_to}
										</div>
									`
								},
								{
									fieldtype: 'Currency',
									fieldname: 'previous_rate',
									label: 'Previous Rate (₹)',
									default: previous_rate,
									read_only: 1   // just for display
								},
								{
									fieldtype: 'Currency',
									fieldname: 'new_rate',
									label: 'New Rate (₹)',
									reqd: 1,
									default: previous_rate  // prefilled, user can edit
								}
							],
							primary_action_label: __('Confirm & Save'),
							primary_action(values) {

								if (values.new_rate === previous_rate) {
									frappe.msgprint({
										message: 'New rate is the same as the previous rate. No changes made.',
										indicator: 'orange'
									});
									return;
								}

								// Set new rate on the form and save
								frm.set_value('rate', values.new_rate);

								frm.save().then(() => {
									dialog.hide();
									frappe.show_alert({
										message: `Rate updated from ₹${previous_rate} 
										          to ₹${values.new_rate} for 
										          ${frm.doc.milk_type} 
										          (Fat ${frm.doc.fat_from}–${frm.doc.fat_to})`,
										indicator: 'green'
									}, 5);
								});
							}
						});

						dialog.show();
					});

			}, __('Actions'));
		}
	}
});
