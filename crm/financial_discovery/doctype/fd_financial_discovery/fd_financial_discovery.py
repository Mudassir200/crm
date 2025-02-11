# Copyright (c) 2024, Oappsit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from crm.financial_discovery.api.financial_discovery import calculateAllFDFields


class FDFinancialDiscovery(Document):

	def validate(self):
		buyers = len(self.buyers)
		if self.household_type == "Single" and buyers != 1:
			frappe.throw("1 buyer is required.")
		elif self.household_type == "Couple" and buyers != 2:
			frappe.throw("At least 2 buyers are required.")

	def before_save(self):
		if self.annual_income_goal > 0:
			self.weekly_income_goal = self.annual_income_goal / 52
		if self.timeframe < 0:
			self.timeframe = 0

		name = ""
		for buyer in self.buyers:
			if name == "":
				name += buyer.first_name + " " + buyer.surname
			else:
				name += " and " + buyer.first_name + " " + buyer.surname

		self.fd_name = name

	def before_insert(self):
		self.user = frappe.session.user
