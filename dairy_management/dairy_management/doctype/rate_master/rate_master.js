// Copyright (c) 2026, jaynasit111@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rate Master", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__('Update Rate'), () => {

				// Fetch the current saved rate from DB (previous rate)
				frappe.db.get_value('Rate Master', frm.doc.name, 'rate')
					.then(r => {
						let previous_rate = r.message.rate;
						let current_rate  = frm.doc.rate;

						// Show confirmation dialog with old vs new rate
						let dialog = new frappe.ui.Dialog({
							title: __('Confirm Rate Update'),
							fields: [
								{
									fieldtype: 'HTML',
									options: `
										<div style="padding: 10px 0">
											<table style="width:100%; border-collapse:collapse; font-size:14px;">
												<tr style="background:#f5f5f5;">
													<th style="padding:10px; border:1px solid #d1d8dd; text-align:left;">Milk Type</th>
													<th style="padding:10px; border:1px solid #d1d8dd; text-align:left;">Fat Range</th>
													<th style="padding:10px; border:1px solid #d1d8dd; text-align:left;">Previous Rate</th>
													<th style="padding:10px; border:1px solid #d1d8dd; text-align:left;">New Rate</th>
												</tr>
												<tr>
													<td style="padding:10px; border:1px solid #d1d8dd;">
														<b>${frm.doc.milk_type}</b>
													</td>
													<td style="padding:10px; border:1px solid #d1d8dd;">
														${frm.doc.fat_from} – ${frm.doc.fat_to}
													</td>
													<td style="padding:10px; border:1px solid #d1d8dd; color:#e74c3c;">
														<b>₹ ${previous_rate}</b>
													</td>
													<td style="padding:10px; border:1px solid #d1d8dd; color:#27ae60;">
														<b>₹ ${current_rate}</b>
													</td>
												</tr>
											</table>
											<p style="margin-top:12px; color:#8D99A6; font-size:12px;">
												⚠️ New Milk Collection entries will automatically 
												use the updated rate. Existing records are unchanged.
											</p>
										</div>
									`
								}
							],
							primary_action_label: __('Confirm & Save'),
							primary_action() {
								frm.save()
									.then(() => {
										dialog.hide();
										frappe.show_alert({
											message: `Rate updated to ₹${current_rate} for 
											          ${frm.doc.milk_type} 
											          (Fat ${frm.doc.fat_from}–${frm.doc.fat_to})`,
											indicator: 'green'
										}, 5);
									});
							},
							secondary_action_label: __('Cancel'),
							secondary_action() {
								dialog.hide();
							}
						});

						dialog.show();
					});

			}, __('Actions'));
		}
	}
});