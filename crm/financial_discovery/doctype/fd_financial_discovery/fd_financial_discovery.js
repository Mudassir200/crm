// Copyright (c) 2024, Oappsit and contributors
// For license information, please see license.txt

frappe.ui.form.on("FD Financial Discovery", {
	refresh(frm) {
        frm.add_custom_button(__("Financial Discovery"), () => {
            window.location = `/crm/financial-discovery/${frm.doc.name}`
        });
	},
    validate: function(frm) {
        let buyers = frm.doc.buyers.length;
        if (frm.doc.household_type == 'Single' && buyers != 1) {
            frappe.msgprint(__('Only 1 buyer is required.'));
            frappe.validated = false;
        } else if (frm.doc.household_type == 'Couple' && buyers != 2) {
            frappe.msgprint(__('At least 2 buyers are required.'));
            frappe.validated = false;
        }
    },
    retirement_age_goal: function(frm) {
        if (frm.doc.retirement_age_goal) {
            if (frm.doc.buyers.length > 0) {
                if (frm.doc.buyers[0].date_of_birth == "") {
                    frm.set_value('timeframe', frm.doc.retirement_age_goal);
                }else{
                    const birthdate = frappe.datetime.str_to_obj(frm.doc.buyers[0].date_of_birth );
                    const today = new Date();
                    const birthDateMillis = new Date(frm.doc.buyers[0].date_of_birth).getTime();
                    const todayMillis = today.getTime();
                    const differenceMillis = todayMillis - birthDateMillis;
                    const differenceDays = Math.floor(differenceMillis / (1000 * 60 * 60 * 24 * 365));
                    let timeframe = frm.doc.retirement_age_goal - differenceDays;
                    const m = today.getMonth() - birthdate.getMonth();
                    if (m > 0 || (m === 0 && today.getDate() > birthdate.getDate())) {
                        timeframe--;
                    }
                    frm.set_value('timeframe', timeframe);
                }
                frm.refresh_field('timeframe')
            }
        }
    }
});
