// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("CRM Deal", {
	refresh(frm) {
		frm.add_web_link(`/crm/deals/${frm.doc.name}`, __("Open in Portal"));
	},
	setup: function(frm) {
        frm.fields_dict['stage'].get_query = function(doc) {
            return {
                filters: {
                    'pipeline': frm.doc.pipeline
                },
                order_by: 'sort asc'
            };
        };
    },
	pipeline: function(frm) {
        frm.set_query('stage', function() {
            return {
                filters: {
                    'pipeline': frm.doc.pipeline
                },
                order_by: 'sort asc'
            };
        });
    }
});
