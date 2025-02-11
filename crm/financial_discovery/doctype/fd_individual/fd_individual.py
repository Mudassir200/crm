# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
from datetime import datetime

class FDIndividual(Document):
	def before_save(self):
		today = datetime.today()
		birth_date = getdate(self.date_of_birth)
		age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
		if age < 0:
			age = 0
		self.age = age

