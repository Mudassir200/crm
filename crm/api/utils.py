import frappe
from frappe import _


@frappe.whitelist()
def get_association_list(dt,name,field,source_doctype,istable,target_field,selected_fields=["name"]):
	if not frappe.has_permission(dt, "read", name):
		frappe.throw(_("Not allowed to read this api"), frappe.PermissionError)

	doc = frappe.get_cached_doc(dt,name)
	
	associations = doc.get(field)

	associations_list = []
	if istable:
		for association in associations:
			if association.get(target_field):
				association = frappe.db.get_value(source_doctype, association.get(target_field),selected_fields,as_dict=True)
				associations_list.append(association)
	else:
		association = frappe.db.get_value(source_doctype, associations,selected_fields,as_dict=True)
		associations_list.append(association)

	return associations_list

@frappe.whitelist()
def add_association(dt,name,field,target_field,value):
	if not frappe.has_permission(dt, "write", name):
		frappe.throw(_("Not allowed to write this api"), frappe.PermissionError)

	doc = frappe.get_cached_doc(dt, name)
	doc.reload()
	doc.append(field, {target_field: value})
	doc.save()

	return True

@frappe.whitelist()
def remove_association(dt,name,field,target_field,value):
	if not frappe.has_permission(dt, "write", name):
		frappe.throw(_("Not allowed to write this api"), frappe.PermissionError)

	doc = frappe.get_cached_doc(dt, name)
	doc.reload()
	association_to_remove = None
	for d in doc.get(field):
		if d.get('name') == value:
			association_to_remove = d
			break
	if association_to_remove:
		doc.get(field).remove(association_to_remove)
	doc.save()

	return True

