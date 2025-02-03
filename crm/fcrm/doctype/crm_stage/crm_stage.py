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


@frappe.whitelist()
def sortExist(pipeline,sort):
    return frappe.db.count('CRM Stage',
			{
				'pipeline': pipeline,
                'sort':sort
			})