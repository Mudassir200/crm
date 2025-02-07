frappe.ui.form.on("CRM Fields Layout", {
    setup: function(frm) {
        frm.fields_dict['association_card'].grid.get_field('association_card').get_query = function() {
            return {
                query: "crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_cards?dt=" + frm.doc.dt,
            };
        };
    },
    dt: function(frm) {
        frm.fields_dict['association_card'].grid.get_field('association_card').get_query = function() {
            return {
                query: "crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_cards?dt=" + frm.doc.dt,
            };
        };
    }
});
