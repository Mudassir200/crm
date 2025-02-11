# Copyright (c) 2024, OPS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FDLiabilities(Document):
	def before_save(self):
		pass
		# if self.limit > 0:
		# 	self.monthly_repayment = self.owning * 3 /100

