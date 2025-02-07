import frappe
from frappe import _


@frappe.whitelist()
def get_association_list(target_doctype,dt,name,source_doctype=None,target_field=None):
	if not frappe.has_permission(dt, "read", name):
		frappe.throw(_("Not allowed to read this api"), frappe.PermissionError)

	associations = frappe.get_all(
		target_doctype,
		filters={"parenttype": dt, "parent": name},
		fields=["*"],
	)
	object_association = []
	keys_to_remove = ["parent","idx","creation","modified","modified_by","owner","docstatus","parenttype","parentfield"]
	for association in associations:
		for key in keys_to_remove: association.pop(key, None)
		# association = frappe.get_doc(source_doctype, association[target_field]).as_dict()
		object_association.append(association)
	

	return object_association

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

