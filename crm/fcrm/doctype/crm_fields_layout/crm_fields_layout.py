# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import json

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import random_string


class CRMFieldsLayout(Document):
	pass


@frappe.whitelist()
def get_fields_layout(doctype: str, type: str, parent_doctype: str | None = None):
	tabs = []
	layout = None

	if frappe.db.exists("CRM Fields Layout", {"dt": doctype, "type": type}):
		layout = frappe.get_doc("CRM Fields Layout", {"dt": doctype, "type": type})

	if layout and layout.layout:
		tabs = json.loads(layout.layout)

	if not tabs:
		tabs = get_default_layout(doctype)

	has_tabs = tabs[0].get("sections") if tabs and tabs[0] else False

	if not has_tabs:
		tabs = [{"name": "first_tab", "sections": tabs}]

	allowed_fields = []
	for tab in tabs:
		for section in tab.get("sections"):
			if "columns" not in section:
				continue
			for column in section.get("columns"):
				if not column.get("fields"):
					continue
				allowed_fields.extend(column.get("fields"))

	fields = frappe.get_meta(doctype).fields
	fields = [field for field in fields if field.fieldname in allowed_fields]

	for tab in tabs:
		for section in tab.get("sections"):
			for column in section.get("columns") if section.get("columns") else []:
				for field in column.get("fields") if column.get("fields") else []:
					field = next((f for f in fields if f.fieldname == field), None)
					if field:
						field = field.as_dict()
						handle_perm_level_restrictions(field, doctype, parent_doctype)
						column["fields"][column.get("fields").index(field["fieldname"])] = field

	return tabs or []


@frappe.whitelist()
def get_sidepanel_sections(doctype,type="Side Panel"):
	if not frappe.db.exists("CRM Fields Layout", {"dt": doctype, "type": type}):
		return []
	layout = frappe.get_doc("CRM Fields Layout", {"dt": doctype, "type":type}).layout

	if not layout:
		return []

	layout = json.loads(layout)

	not_allowed_fieldtypes = [
		"Tab Break",
		"Section Break",
		"Column Break",
	]

	fields = frappe.get_meta(doctype).fields
	fields = [field for field in fields if field.fieldtype not in not_allowed_fieldtypes]

	for section in layout:
		section["name"] = section.get("name") or section.get("label")
		for column in section.get("columns") if section.get("columns") else []:
			for field in column.get("fields") if column.get("fields") else []:
				field_obj = next((f for f in fields if f.fieldname == field), None)
				if field_obj:
					field_obj = field_obj.as_dict()
					handle_perm_level_restrictions(field_obj, doctype)
					column["fields"][column.get("fields").index(field)] = get_field_obj(field_obj)

	fields_meta = {}
	for field in fields:
		fields_meta[field.fieldname] = field

	return layout


@frappe.whitelist()
def get_right_sidepanel_sections(doctype,type="Right Side Panel"):
	if not frappe.db.exists("CRM Fields Layout", {"dt": doctype, "type": type}):
		return []
	cards = frappe.get_doc("CRM Fields Layout", {"dt": doctype, "type":type}).association_card
	if not cards:
		return []

	layout = []

	for card in cards:
		card_details = frappe.get_doc("CRM Association Card", card.get("association_card"))
		fields = frappe.get_meta(card_details.get("source_doctype")).fields
		selected_fields = json.loads(card_details.get("selected_fields"))
		selected_fields_keys = [card_details.get("title_field")]
		for field in selected_fields:
			selected_fields_keys.append(list(field.keys())[0])

		# selected_fields_keys is sorted by own display order
		fields = sorted(
			[field for field in fields if field.fieldname in selected_fields_keys],
			key=lambda x: selected_fields_keys.index(x.fieldname) if x.fieldname in selected_fields_keys else len(selected_fields_keys)
		)
		
		layout.append({
			"name": card_details.get("name"),
			"label": card.get("section_title"),
			"source_doctype": card_details.get("source_doctype"),
			"target_doctype": card_details.get("target_doctype"),
			"target_field": card_details.get("target_field"),
			"reference_field": card_details.get("reference_field"),
			"title_field": card_details.get("title_field"),
			"selected_fields": selected_fields_keys,
			"empty_message": card_details.get("empty_section_message"),
			"istable": card_details.get("is_child_table"),
			"route": card_details.get("route"),
			"opened": True,
			"editable": False,
			"visible": True,
			"fields":fields,
			"data":False
		})

	return layout


def handle_perm_level_restrictions(field, doctype, parent_doctype=None):
	if field.permlevel == 0:
		return
	field_has_write_access = field.permlevel in get_permlevel_access("write", doctype, parent_doctype)
	field_has_read_access = field.permlevel in get_permlevel_access("read", doctype, parent_doctype)

	if not field_has_write_access and field_has_read_access:
		field.read_only = 1
	if not field_has_read_access and not field_has_write_access:
		field.hidden = 1


def get_permlevel_access(permission_type="write", doctype=None, parent_doctype=None):
	allowed_permlevels = []
	roles = frappe.get_roles()

	meta = frappe.get_meta(doctype)

	if meta.istable and parent_doctype:
		meta = frappe.get_meta(parent_doctype)
	elif meta.istable and not parent_doctype:
		return [1, 0]

	for perm in meta.permissions:
		if perm.role in roles and perm.get(permission_type) and perm.permlevel not in allowed_permlevels:
			allowed_permlevels.append(perm.permlevel)

	return allowed_permlevels


def get_field_obj(field):
	field["placeholder"] = field.get("placeholder") or "Add " + field.label + "..."

	if field.fieldtype == "Link":
		field["placeholder"] = field.get("placeholder") or "Select " + field.label + "..."
	elif field.fieldtype == "Select" and field.options:
		field["placeholder"] = field.get("placeholder") or "Select " + field.label + "..."
		field["options"] = [{"label": option, "value": option} for option in field.options.split("\n")]

	if field.read_only:
		field["tooltip"] = "This field is read only and cannot be edited."

	return field


@frappe.whitelist()
def save_fields_layout(doctype: str, type: str, layout: str):
	if frappe.db.exists("CRM Fields Layout", {"dt": doctype, "type": type}):
		doc = frappe.get_doc("CRM Fields Layout", {"dt": doctype, "type": type})
	else:
		doc = frappe.new_doc("CRM Fields Layout")

	doc.update(
		{
			"dt": doctype,
			"type": type,
			"layout": layout,
		}
	)
	doc.save(ignore_permissions=True)

	return doc.layout


def get_default_layout(doctype: str):
	fields = frappe.get_meta(doctype).fields

	tabs = []

	if fields and fields[0].fieldtype != "Tab Break":
		sections = []
		if fields and fields[0].fieldtype != "Section Break":
			sections.append(
				{
					"name": "section_" + str(random_string(4)),
					"columns": [{"name": "column_" + str(random_string(4)), "fields": []}],
				}
			)
		tabs.append({"name": "tab_" + str(random_string(4)), "sections": sections})

	for field in fields:
		if field.fieldtype == "Tab Break":
			tabs.append(
				{
					"name": "tab_" + str(random_string(4)),
					"sections": [
						{
							"name": "section_" + str(random_string(4)),
							"columns": [{"name": "column_" + str(random_string(4)), "fields": []}],
						}
					],
				}
			)
		elif field.fieldtype == "Section Break":
			tabs[-1]["sections"].append(
				{
					"name": "section_" + str(random_string(4)),
					"columns": [{"name": "column_" + str(random_string(4)), "fields": []}],
				}
			)
		elif field.fieldtype == "Column Break":
			tabs[-1]["sections"][-1]["columns"].append(
				{"name": "column_" + str(random_string(4)), "fields": []}
			)
		else:
			tabs[-1]["sections"][-1]["columns"][-1]["fields"].append(field.fieldname)

	return tabs

@frappe.whitelist()
def get_cards(dt):
    return frappe.db.get_list('CRM Association Card',
			filters={
				'reference_doctype': dt,
                'enabled':1
			},
			fields=["name as value","section_title as label"]
		)