# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CRMStage(Document):
	def validate(self):
		exist = sortExist(self.pipeline,self.sort)
		sort = frappe.db.get_value('CRM Stage', self.name, 'sort')
		if sort != self.sort and exist > 0:
			frappe.throw("Sort already exist")

		stage_name = frappe.db.get_value('CRM Stage', self.name, 'stage_name')

		exist = frappe.db.exists('CRM Stage', {'stage_name':self.stage_name,"pipeline":self.pipeline})
		if exist and self.stage_name != stage_name:
			frappe.throw("Stage Name Already Exist with Selected Pipeline!")
	
	def after_insert(self):
		doc = self
		fields_to_create = [
			{
				"fieldname": f"date_entered_in_{doc.name}",
				"label": f'Date Entered in "{doc.stage_name} ({doc.pipeline})"',
				"fieldtype": "Datetime",
				"insert_after": "stage",
				"read_only": 1
			},
			{
				"fieldname": f"date_exited_in_{doc.name}",
				"label": f'Date Exited in "{doc.stage_name} ({doc.pipeline})"',
				"fieldtype": "Datetime",
				"insert_after": f"date_entered_in_{doc.name}",
				"read_only": 1
			},
			{
				"fieldname": f"cumulative_time_in_{doc.name}",
				"label": f'Cumulative Time in "{doc.stage_name} ({doc.pipeline})"',
				"fieldtype": "Int",
				"insert_after": f"date_exited_in_{doc.name}",
				"read_only": 1
			},
			{
				"fieldname": f"latest_time_in_{doc.name}",
				"label": f'Latest Time in "{doc.stage_name} ({doc.pipeline})"',
				"fieldtype": "Int",
				"insert_after": f"cumulative_time_in_{doc.name}",
				"read_only": 1
			}
		]
		for field in fields_to_create:
			if not frappe.db.exists("Custom Field", {"dt": "CRM Deal", "fieldname": field["fieldname"]}):
				custom_field = frappe.get_doc({
					"doctype": "Custom Field",
					"dt": "CRM Deal",
					"fieldname": field["fieldname"],
					"label": field["label"],
					"fieldtype": field["fieldtype"],
					"insert_after": field["insert_after"],
					"read_only": field.get("read_only", 0)
				})
				custom_field.insert()
	

		

@frappe.whitelist()
def sortExist(pipeline,sort):
    return frappe.db.count('CRM Stage', {'pipeline': pipeline,'sort':sort})