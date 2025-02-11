// Copyright (c) 2024, OPS and contributors
// For license information, please see license.txt

frappe.ui.form.on("FD Liabilities", {
	refresh(frm) {

	},
    owning: function(frm) {
        if (frm.doc.owning && frm.doc.limit > 0 ) {
            frm.set_value('monthly_repayment', frm.doc.owning * 3 / 100);
            frm.refresh_field('monthly_repayment')
        }
    }
});
