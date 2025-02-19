import json

import frappe
from frappe import _
from frappe.model import no_value_fields
from frappe.model.document import get_controller
from frappe.utils import make_filter_tuple
from pypika import Criterion

from crm.api.views import get_views
from crm.fcrm.doctype.crm_form_script.crm_form_script import get_form_script

@frappe.whitelist()
def get_data(
	doctype: str,
	filters: list,
	order_by: str,
	page_length=20,
	page_length_count=20,
	column_field=None,
	title_field=None,
	columns=[],
	rows=[],
	kanban_columns=[],
	kanban_fields=[],
	view=None,
	default_filters=None,
):
	custom_view = False
	# filters = frappe._dict(filters)
	rows = frappe.parse_json(rows or "[]")
	columns = frappe.parse_json(columns or "[]")
	kanban_fields = frappe.parse_json(kanban_fields or "[]")
	kanban_columns = frappe.parse_json(kanban_columns or "[]")
	custom_view_name = view.get("custom_view_name") if view else None
	view_type = view.get("view_type") if view else None
	group_by_field = view.get("group_by_field") if view else None


	# for key in filters:
	# 	value = filters[key]
	# 	if isinstance(value, list):
	# 		if "@me" in value:
	# 			value[value.index("@me")] = frappe.session.user
	# 		elif "%@me%" in value:
	# 			index = [i for i, v in enumerate(value) if v == "%@me%"]
	# 			for i in index:
	# 				value[i] = "%" + frappe.session.user + "%"
	# 	elif value == "@me":
	# 		filters[key] = frappe.session.user

	pipelineFilters = {}
	# if view_type == "kanban" and column_field == "stage":
	# 	if "pipeline" in filters:
	# 		pipelineFilters['pipeline'] = filters.get("pipeline")
	# 	else:
	# 		pipelineList = frappe.db.get_list("CRM Pipeline",order_by='sort asc')
	# 		if len(pipelineList) > 0:
	# 			pipelineFilters['pipeline'] = pipelineList[0].name


	if default_filters:
		default_filters = frappe.parse_json(default_filters)
		filters.update(default_filters)

	is_default = True
	data = []
	_list = get_controller(doctype)
	default_rows = []
	if hasattr(_list, "default_list_data"):
		default_rows = _list.default_list_data().get("rows")

	if view_type != "kanban":
		if columns or rows:
			custom_view = True
			is_default = False
			columns = frappe.parse_json(columns)
			rows = frappe.parse_json(rows)

		if not columns:
			columns = [
				{"label": "Name", "type": "Data", "key": "name", "width": "16rem"},
				{"label": "Last Modified", "type": "Datetime", "key": "modified", "width": "8rem"},
			]

		if not rows:
			rows = ["name"]

		default_view_filters = {
			"dt": doctype,
			"type": view_type or "list",
			"is_default": 1,
			"user": frappe.session.user,
		}

		if not custom_view and frappe.db.exists("CRM View Settings", default_view_filters):
			list_view_settings = frappe.get_doc("CRM View Settings", default_view_filters)
			columns = frappe.parse_json(list_view_settings.columns)
			rows = frappe.parse_json(list_view_settings.rows)
			is_default = False
		elif not custom_view or (is_default and hasattr(_list, "default_list_data")):
			rows = default_rows
			columns = _list.default_list_data().get("columns")

		# check if rows has all keys from columns if not add them
		for column in columns:
			if column.get("key") not in rows:
				rows.append(column.get("key"))
			column["label"] = _(column.get("label"))

			if column.get("key") == "_liked_by" and column.get("width") == "10rem":
				column["width"] = "50px"

		# check if rows has group_by_field if not add it
		if group_by_field and group_by_field not in rows:
			rows.append(group_by_field)

		# data = (
		# 	frappe.get_list(
		# 		doctype,
		# 		fields=rows,
		# 		filters=filters,
		# 		order_by=order_by,
		# 		page_length=page_length,
		# 	)
		# 	or []
		# )
		
		data = (
			get_dynamic_grouped_data(doctype,rows,filters,order_by,page_length)		
			or []
		)
		data = parse_list_data(data, doctype)

	if view_type == "kanban":
		if not rows:
			rows = default_rows

		if (not kanban_columns or column_field == "stage") and column_field:
			field_meta = frappe.get_meta(doctype).get_field(column_field)
			if field_meta.fieldtype == "Link":
				if column_field == "stage":
					kanban_columns = frappe.get_all(
						field_meta.options,
						filters=pipelineFilters,
						fields=["name as name","stage_name","pipeline"],
						order_by="sort asc",
					)
				else:
					kanban_columns = frappe.get_all(
						field_meta.options,
						fields=["name"],
						order_by="modified asc",
					)
			elif field_meta.fieldtype == "Select":
				kanban_columns = [{"name": option} for option in field_meta.options.split("\n")]

		if not title_field:
			title_field = "name"
			if hasattr(_list, "default_kanban_settings"):
				title_field = _list.default_kanban_settings().get("title_field")

		if title_field not in rows:
			rows.append(title_field)

		if not kanban_fields:
			kanban_fields = ["name"]
			if hasattr(_list, "default_kanban_settings"):
				kanban_fields = json.loads(_list.default_kanban_settings().get("kanban_fields"))

		for field in kanban_fields:
			if field not in rows:
				rows.append(field)

		for kc in kanban_columns:
			column_filters = {column_field: kc.get("name")}
			order = kc.get("order")
			if (column_field in filters and filters.get(column_field) != kc.get("name")) or kc.get("delete"):
				column_data = []
			else:
				column_filters.update(filters.copy())
				page_length = 20

				if kc.get("page_length"):
					page_length = kc.get("page_length")

				if order:
					column_data = get_records_based_on_order(
						doctype, rows, column_filters, page_length, order
					)
				else:
					column_data = frappe.get_list(
						doctype,
						fields=rows,
						filters=convert_filter_to_tuple(doctype, column_filters),
						order_by=order_by,
						page_length=page_length,
					)

				new_filters = filters.copy()
				new_filters.update({column_field: kc.get("name")})

				all_count = len(
					frappe.get_list(doctype, filters=convert_filter_to_tuple(doctype, new_filters))
				)

				kc["all_count"] = all_count
				kc["count"] = len(column_data)

				for d in column_data:
					getCounts(d, doctype)

			if order:
				column_data = sorted(
					column_data,
					key=lambda x: order.index(x.get("name")) if x.get("name") in order else len(order),
				)

			data.append({"column": kc, "fields": kanban_fields, "data": column_data})

	fields = frappe.get_meta(doctype).fields
	fields = [field for field in fields if field.fieldtype not in no_value_fields]
	fields = [
		{
			"label": _(field.label),
			"fieldtype": field.fieldtype,
			"fieldname": field.fieldname,
			"options": field.options,
		}
		for field in fields
		if field.label and field.fieldname
	]

	std_fields = [
		{"label": "Name", "fieldtype": "Data", "fieldname": "name"},
		{"label": "Created On", "fieldtype": "Datetime", "fieldname": "creation"},
		{"label": "Last Modified", "fieldtype": "Datetime", "fieldname": "modified"},
		{
			"label": "Modified By",
			"fieldtype": "Link",
			"fieldname": "modified_by",
			"options": "User",
		},
		{"label": "Assigned To", "fieldtype": "Text", "fieldname": "_assign"},
		{"label": "Owner", "fieldtype": "Link", "fieldname": "owner", "options": "User"},
		{"label": "Like", "fieldtype": "Data", "fieldname": "_liked_by"},
	]

	for field in std_fields:
		if field.get("fieldname") not in rows:
			rows.append(field.get("fieldname"))
		if field not in fields:
			field["label"] = _(field["label"])
			fields.append(field)

	if not is_default and custom_view_name:
		is_default = frappe.db.get_value("CRM View Settings", custom_view_name, "load_default_columns")

	if group_by_field and view_type == "group_by":

		def get_options(type, options):
			if type == "Select":
				return [option for option in options.split("\n")]
			else:
				has_empty_values = any([not d.get(group_by_field) for d in data])
				options = list(set([d.get(group_by_field) for d in data]))
				options = [u for u in options if u]
				if has_empty_values:
					options.append("")

				if order_by and group_by_field in order_by:
					order_by_fields = order_by.split(",")
					order_by_fields = [
						(field.split(" ")[0], field.split(" ")[1]) for field in order_by_fields
					]
					if (group_by_field, "asc") in order_by_fields:
						options.sort()
					elif (group_by_field, "desc") in order_by_fields:
						options.sort(reverse=True)
				else:
					options.sort()
				return options

		for field in fields:
			if field.get("fieldname") == group_by_field:
				group_by_field = {
					"label": field.get("label"),
					"fieldname": field.get("fieldname"),
					"fieldtype": field.get("fieldtype"),
					"options": get_options(field.get("fieldtype"), field.get("options")),
				}

	return {
		"data": data,
		"columns": columns,
		"rows": rows,
		"fields": fields,
		"column_field": column_field,
		"title_field": title_field,
		"kanban_columns": kanban_columns,
		"kanban_fields": kanban_fields,
		"group_by_field": group_by_field,
		"page_length": page_length,
		"page_length_count": page_length_count,
		"is_default": is_default,
		"views": get_views(doctype),
		"total_count": len(get_dynamic_grouped_data(doctype,fields=["name"],filters=filters)),
		"row_count": len(data),
		"form_script": get_form_script(doctype),
		"list_script": get_form_script(doctype, "List"),
		"view_type": view_type,
	}

def get_dynamic_grouped_data(doctype, fields, filters, order_by="modified desc", page_length=20, page=1):
	selected_fields = ", ".join([f"`{field}`" for field in fields if field]) if fields else "*"
		
	conditions = []
	params = []

	for group in filters:
		group_conditions = []
		for condition in group:
			field = condition[0]
			operator = condition[1]
			value = condition[2]

			group_conditions.append(f"`{field}` {operator} %s")
			params.append(value)

		conditions.append("(" + " AND ".join(group_conditions) + ")")

	where_clause = " OR ".join(conditions) if conditions else "1=1"

	order_clause = f"ORDER BY {order_by}" if order_by else ""

	offset = (page - 1) * page_length
	limit_clause = f"LIMIT {page_length} OFFSET {offset}" if page_length > 0 else ""

	query = f"""
		SELECT {selected_fields}
		FROM `tab{doctype}`
		WHERE {where_clause}
		GROUP BY {selected_fields}
		{order_clause}
		{limit_clause}
	"""
	frappe.log_error("query",query)

	data = frappe.db.sql(query, tuple(params), as_dict=True)
	return data




def parse_list_data(data, doctype):
	_list = get_controller(doctype)
	if hasattr(_list, "parse_list_data"):
		data = _list.parse_list_data(data)
	return data


def convert_filter_to_tuple(doctype, filters):
	if isinstance(filters, dict):
		filters_items = filters.items()
		filters = []
		for key, value in filters_items:
			filters.append(make_filter_tuple(doctype, key, value))
	return filters


def get_records_based_on_order(doctype, rows, filters, page_length, order):
	records = []
	filters = convert_filter_to_tuple(doctype, filters)
	in_filters = filters.copy()
	in_filters.append([doctype, "name", "in", order[:page_length]])
	records = frappe.get_list(
		doctype,
		fields=rows,
		filters=in_filters,
		order_by="creation desc",
		page_length=page_length,
	)

	if len(records) < page_length:
		not_in_filters = filters.copy()
		not_in_filters.append([doctype, "name", "not in", order])
		remaining_records = frappe.get_list(
			doctype,
			fields=rows,
			filters=not_in_filters,
			order_by="creation desc",
			page_length=page_length - len(records),
		)
		for record in remaining_records:
			records.append(record)

	return records


def getCounts(d, doctype):
	d["_email_count"] = (
		frappe.db.count(
			"Communication",
			filters={
				"reference_doctype": doctype,
				"reference_name": d.get("name"),
				"communication_type": "Communication",
			},
		)
		or 0
	)
	d["_email_count"] = d["_email_count"] + frappe.db.count(
		"Communication",
		filters={
			"reference_doctype": doctype,
			"reference_name": d.get("name"),
			"communication_type": "Automated Message",
		},
	)
	d["_comment_count"] = frappe.db.count(
		"Comment",
		filters={"reference_doctype": doctype, "reference_name": d.get("name"), "comment_type": "Comment"},
	)
	d["_task_count"] = frappe.db.count(
		"CRM Task", filters={"reference_doctype": doctype, "reference_docname": d.get("name")}
	)
	d["_note_count"] = frappe.db.count(
		"FCRM Note", filters={"reference_doctype": doctype, "reference_docname": d.get("name")}
	)
	return d
