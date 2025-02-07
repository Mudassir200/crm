# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CRMAssociationCard(Document):
	pass

# Add Fuction for get Fields by doctype
@frappe.whitelist()
def get_fields(dt):
    fields = frappe.db.get_list('DocField',
			filters={
				'parent': dt,
			},
			fields=["*"]
		)
    not_allowed_type = ["Section Break","Tab Break","Column Break"]
    fields = [field for field in fields if field.get('fieldtype') not in not_allowed_type]
    fields = [{"label":field.get('label'),"value":field.get("fieldname")} for field in fields]
    return fields