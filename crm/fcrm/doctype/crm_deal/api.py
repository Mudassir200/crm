import frappe

from crm.api.doc import get_assigned_users, get_fields_meta
from crm.fcrm.doctype.crm_form_script.crm_form_script import get_form_script


@frappe.whitelist()
def get_deal(name):
	deal = frappe.get_doc("CRM Deal", name).as_dict()

	deal["fields_meta"] = get_fields_meta("CRM Deal")
	deal["_form_script"] = get_form_script("CRM Deal")
	deal["_assign"] = get_assigned_users("CRM Deal", deal.name)
	return deal


@frappe.whitelist()
def get_deal_contacts(name):
	contacts = frappe.get_all(
		"CRM Contacts",
		filters={"parenttype": "CRM Deal", "parent": name},
		fields=["contact", "is_primary"],
	)
	deal_contacts = []
	for contact in contacts:
		is_primary = contact.is_primary
		contact = frappe.get_doc("Contact", contact.contact).as_dict()

		def get_primary_email(contact):
			for email in contact.email_ids:
				if email.is_primary:
					return email.email_id
			return contact.email_ids[0].email_id if contact.email_ids else ""

		def get_primary_mobile_no(contact):
			for phone in contact.phone_nos:
				if phone.is_primary:
					return phone.phone
			return contact.phone_nos[0].phone if contact.phone_nos else ""

		_contact = {
			"name": contact.name,
			"image": contact.image,
			"full_name": contact.full_name,
			"email": get_primary_email(contact),
			"mobile_no": get_primary_mobile_no(contact),
			"is_primary": is_primary,
		}
		deal_contacts.append(_contact)
	return deal_contacts


@frappe.whitelist()
def get_deal_property(name):
	properties = frappe.get_all(
		"CRM Deal Propety",
		filters={"parenttype": "CRM Deal", "parent": name},
		fields=["propety"],
	)
	deal_properties = []
	for property in properties:
		property = frappe.get_doc("Realestate Property", property.propety).as_dict()

		_property = {
			"name": property.name,
			"image": property.image,
			"property_name": property.property_name,
			"property_type": property.property_type,
			"lot_no": property.lot_no,
			"property_status": property.property_status,
			"dwelling_type": property.dwelling_type,
			"contract_type": property.contract_type,
			"bedrooms": property.bedrooms,
			"bathrooms": property.bathrooms,
			"total_price": property.total_price
		}
		deal_properties.append(_property)
	return deal_properties