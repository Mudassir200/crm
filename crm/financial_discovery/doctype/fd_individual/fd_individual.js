// Copyright (c) 2024, OPS and contributors
// For license information, please see license.txt

frappe.ui.form.on("FD Individual", {
	refresh(frm) {

	},
    date_of_birth: function(frm) {
        if (frm.doc.date_of_birth) {
            const birthdate = frappe.datetime.str_to_obj(frm.doc.date_of_birth);
            const today = frappe.datetime.now_date(true);
            let age = today.getFullYear() - birthdate.getFullYear();
            const m = today.getMonth() - birthdate.getMonth();
            if (m < 0 || (m === 0 && today.getDate() < birthdate.getDate())) {
                age--;
            }
            frm.set_value('age', age);
            frm.refresh_field('age')
        }
    }
});
