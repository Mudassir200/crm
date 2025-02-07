// Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("CRM Association Card", {
	setup: function(frm) {
        frm.fields_dict['target_field'].get_query = function(doc) {
            return {
                query: "crm.fcrm.doctype.crm_association_card.crm_association_card.get_fields?dt=" + frm.doc.target_doctype,
            };
        };
        frm.fields_dict['reference_field'].get_query = function(doc) {
            return {
                query: "crm.fcrm.doctype.crm_association_card.crm_association_card.get_fields?dt=" + frm.doc.reference_doctype,
            };
        };
    },
	target_doctype: function(frm) {
        frm.fields_dict['target_field'].get_query =  function() {
            return {
                query: "crm.fcrm.doctype.crm_association_card.crm_association_card.get_fields?dt=" + frm.doc.target_doctype,
            };
        };
    },
    reference_doctype: function(frm) {
        frm.fields_dict['reference_field'].get_query = function(doc) {
            return {
                query: "crm.fcrm.doctype.crm_association_card.crm_association_card.get_fields?dt=" + frm.doc.reference_doctype,
            };
        };
    }
});
