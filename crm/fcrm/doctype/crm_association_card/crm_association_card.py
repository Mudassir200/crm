# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CRMAssociationCard(Document):
	pass

@frappe.whitelist()
def get_fields(dt):
    fields = frappe.db.get_list('DocField',
			filters={
				'parent': dt,
			},
			fields=["*"]
		)
    not_allowed_type = ["Section Break","Tab Break","Column Break","Table","Table Multiselect"]
    fields = [field for field in fields if field.get('fieldtype') not in not_allowed_type]
    fields = [{"label":field.get('label'),"value":field.get("fieldname")} for field in fields]
    return fields

@frappe.whitelist()
def get_link_fields(dt,source=None):
    fields = frappe.db.get_list('DocField',
			filters={
				'parent': dt,
			},
			fields=["*"]
		)
    allowed_type = ["Link","Table","Table Multiselect"]
    fields = [field for field in fields if field.get('fieldtype') in allowed_type]
    
    if source:
        fields = [field for field in fields if field.get('options') == source]
        
    fields = [{"label":field.get('label'),"value":field.get("fieldname"),"options":field.get("options")} for field in fields]
    return fields


@frappe.whitelist()
def is_child_doctype(dt):
    return frappe.db.get_value('DocType',{'name': dt},'istable')