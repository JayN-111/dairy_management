frappe.pages['dairy-summary-board'].on_page_load = function (wrapper) {
	let page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Dairy Summary Board',
		single_column: true
	});

	$(wrapper).find('.layout-main-section').html(
		frappe.render_template('dairy_summary_board', {})
	);

	load_summary();
};


function load_summary() {
	let from_date = $('#from_date').val() || null;
	let to_date = $('#to_date').val() || null;

	frappe.call({
		method: 'dairy_management.dairy_management.page.dairy_summary_board.dairy_summary_board.get_summary',
		args: { from_date, to_date },
		callback(r) {
			if (!r.message) return;

			let d = r.message;

			// Buy
			// $('#buy_ltr').text(frappe.utils.format_number(d.buy_ltr, null, 2) + ' Ltr');
			// $('#buy_price').text('₹ ' + frappe.utils.format_number(d.buy_price, null, 2));
			$('#buy_ltr').text(
				d.buy_ltr !== undefined ? d.buy_ltr + ' Ltr' : '—'
			);
			$('#buy_price').text(
				d.buy_price !== undefined ? '₹ ' + d.buy_price : '₹ 0.00'
			);

			// Sale
			// $('#sale_ltr').text(frappe.utils.format_number(d.sale_ltr, null, 2) + ' Ltr');
			// $('#sale_price').text('₹ ' + frappe.utils.format_number(d.sale_price, null, 2));
			$('#sale_ltr').text(
				d.sale_ltr !== undefined ? d.sale_ltr + ' Ltr' : '—'
			);
			$('#sale_price').text(
				d.sale_price !== undefined ? '₹ ' + d.sale_price : '₹ 0.00'
			);

			// Pending
			let pending = d.pending_ltr;
			$('#pending_ltr').text(
				(d.pending_ltr !== undefined ? d.pending_ltr : 0) + ' Ltr'
			);
			let card = $('#pending_stock_card');
			let btn = $('#stock_entry_btn');

			if (pending <= 0) {
				card.css('border-color', '#e74c3c');
				$('#pending_ltr').css('color', '#e74c3c');

				btn.removeClass('btn-warning').addClass('btn-danger');
				btn.text('📦 Create Stock Entry (Shortage)');
			}
			else if (pending < 50) {
				card.css('border-color', '#ff9800');
				$('#pending_ltr').css('color', '#ff9800');

				btn.removeClass('btn-danger').addClass('btn-warning');
				btn.text('📦 Create Stock Entry');
			}
			else {
				card.css('border-color', '#4CAF50');
				$('#pending_ltr').css('color', '#4CAF50');

				btn.removeClass('btn-danger btn-warning');
				btn.text('📦 Create Stock Entry');
			}
		}
	});
}


function clear_filter() {
	$('#from_date').val('');
	$('#to_date').val('');
	load_summary();
}


function create_stock_entry() {
	let pending = parseFloat(
		$('#pending_ltr').text().replace(' Ltr', '').replace(/,/g, '')
	);

	// Always allow stock entry
	frappe.new_doc('Stock Entry', {
		stock_entry_type: 'Material Transfer',
		remarks: pending < 0
			? `Shortage Adjustment — ${pending} Ltr`
			: `Dairy Stock Transfer — ${pending} Ltr`
	});
}