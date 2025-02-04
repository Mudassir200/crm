# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CRMPipeline(Document):
	def validate(self):
		exist = sortExist(self.sort)
		sort = frappe.db.get_value('Pipeline', self.name, 'sort')
		if sort != self.sort and exist > 0:
			frappe.throw("Sort already exist")
		
		pipeline_name = frappe.db.get_value('Pipeline', self.name, 'pipeline_name')

		exist = frappe.db.exists('Pipeline', {'pipeline_name':self.pipeline_name})
		if exist and self.pipeline_name != pipeline_name:
			frappe.throw("Pipeline Name Already Exist with Contract Type!")


@frappe.whitelist()
def sortExist(sort):
    return frappe.db.count('CRM Pipeline',{'sort':sort})