frappe.ui.form.on("CRM Association Card", {
	setup: function(frm) {
        frm.fields_dict['target_field'].get_query = function(doc) {
            return {
                query: "crm.fcrm.doctype.crm_association_card.crm_association_card.get_link_fields?dt=" + frm.doc.target_doctype + "&source=" + frm.doc.source_doctype,
            };
        };
        
        frm.fields_dict['reference_field'].get_query = function(doc) {
            return {
                query: "crm.fcrm.doctype.crm_association_card.crm_association_card.get_link_fields?dt=" + frm.doc.reference_doctype,
            };
        };

        frm.fields_dict['title_field'].get_query = function(doc) {
            return {
                query: "crm.fcrm.doctype.crm_association_card.crm_association_card.get_fields?dt=" + frm.doc.source_doctype,
            };
        };
        frm.fields_dict['select_field'].get_query = function(doc) {
            return {
                query: "crm.fcrm.doctype.crm_association_card.crm_association_card.get_fields?dt=" + frm.doc.source_doctype,
            };
        };
        let html = refreshFields(frm.doc.selected_fields)
        frm.fields_dict.selected_fields_html.df.options = html;
        frm.refresh_field('selected_fields_html');
    },
    reference_field: function(frm) {
        frm.fields_dict['reference_field']._data?.forEach(element => {
            if(element.value == frm.doc.reference_field) {
                 isChildTable(element.options).then((result) => {
                    if (result.message) {
                        frm.doc.target_doctype = element.options;
                        frm.refresh_field('target_doctype');
                        frm.doc.is_child_table = 1;
                        frm.refresh_field('is_child_table');
                        frm.doc.source_doctype = "";
                        frm.refresh_field('source_doctype');
                    }else{
                        frm.doc.source_doctype = element.options;
                        frm.refresh_field('source_doctype');
                        frm.doc.is_child_table = 0;
                        frm.refresh_field('is_child_table');
                        frm.doc.target_doctype = "";
                        frm.refresh_field('target_doctype');
                        frm.doc.target_field = "";
                        frm.refresh_field('target_field');
                    }
                 });
            }
        });      
    },        
	target_doctype: function(frm) {
        frm.fields_dict['target_field'].get_query =  function() {
            return {
                query: "crm.fcrm.doctype.crm_association_card.crm_association_card.get_link_fields?dt=" + frm.doc.target_doctype + "&source=" + frm.doc.source_doctype,
            };
        };
    },
    source_doctype: function(frm) {
        frm.fields_dict['target_field'].get_query =  function() {
            return {
                query: "crm.fcrm.doctype.crm_association_card.crm_association_card.get_link_fields?dt=" + frm.doc.target_doctype + "&source=" + frm.doc.source_doctype,
            };
        };
        frm.fields_dict['title_field'].get_query = function(doc) {
            return {
                query: "crm.fcrm.doctype.crm_association_card.crm_association_card.get_fields?dt=" + frm.doc.source_doctype,
            };
        };
        frm.fields_dict['select_field'].get_query = function(doc) {
            return {
                query: "crm.fcrm.doctype.crm_association_card.crm_association_card.get_fields?dt=" + frm.doc.source_doctype,
            };
        };
    },
    reference_doctype: function(frm) {
        frm.fields_dict['reference_field'].get_query = function(doc) {
            return {
                query: "crm.fcrm.doctype.crm_association_card.crm_association_card.get_link_fields?dt=" + frm.doc.reference_doctype,
            };
        };
    },
    select_field: function(frm) {
        let existingFields = frm.doc.selected_fields ? JSON.parse(frm.doc.selected_fields) : [];
        let fields = {}

        let data_options = frm.fields_dict.select_field._data;
        var selectedOption = data_options.find(option => option.value === frm.doc.select_field);
        fields[frm.doc.select_field] = selectedOption.label

        existingFields.push(fields);
        frm.doc.selected_fields = JSON.stringify(existingFields);


        frm.refresh_field('selected_fields');
        let html = refreshFields(frm.doc.selected_fields)

        frm.fields_dict.selected_fields_html.df.options = html;
        frm.refresh_field('selected_fields_html');
        frm.doc.select_field = ""
        frm.refresh_field('select_field');
    }

});

async function isChildTable(dt) {
    return await frappe.call({
        method: `crm.fcrm.doctype.crm_association_card.crm_association_card.is_child_doctype`,
        args: {
            dt: dt
        }
    });
}

$(document).on('click', '.remove-field', function() {
    var fieldId = $(this).data('field-id');
    frm = cur_frm
    if(frm.doc.selected_fields){
        let stages = JSON.parse(frm.doc.selected_fields)
        let index = stages.findIndex(option =>  Object.keys(option)[0] === String(fieldId));
        if (index !== -1) {
            stages.splice(index, 1);
        }
        frm.doc.selected_fields = JSON.stringify(stages);
        frm.refresh_field('selected_fields');
        let html = refreshFields(frm.doc.selected_fields)
    
        frm.fields_dict.selected_fields_html.df.options = html;
        frm.refresh_field('selected_fields_html');
    }
});

function refreshFields(fields){
    let selected_fields = JSON.parse(fields);
    let html = '<ul style="margin: 0 auto;list-style: none;padding: 0;">'
    selected_fields.forEach(element => {
        for (const [key, value] of Object.entries(element)) {
            html += `<li style="background: #000;display: inline-block; padding: 2px 10px;background: #ededed;margin-bottom: 8px; margin-right: 8px;border-radius: 8px;
        ">
                    ${value} 
                    <Button data-field-id="${key}" class="remove-field" style="border: 0;background: none;">
                        <span class="filter-icon">
                            <svg class="es-icon es-line  icon-sm" style="">
                                <use class="" href="#es-small-close"></use>
                            </svg>
                        </span>
                    </Button>
                </li>`
        }
    });
    html += '</ul>'
    return html
}