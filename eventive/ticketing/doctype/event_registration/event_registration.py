# Copyright (c) 2026, Munene Morris and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EventRegistration(Document):
	def validate(self):
		if not self.attendees:
			frappe.throw("Please add at least one attendee to register.")
		else:
			self.set_total()
			self.create_event_tickets()

	def on_submit(self):
		pass

	def set_total(self):
		self.total_amount = sum(
			attendee.ticket_price + attendee.get_merchandise_total()
			for attendee in self.attendees
		)

	def create_event_tickets(self):
		for attendee in self.attendees:
			try:
				ticket = frappe.get_doc({
					"doctype": "Event Ticket",
					"registration": self.name,
					"ticket_type": attendee.ticket_type,
					"email": attendee.email,
					"event": self.event,
				})

				if attendee.merchandise:
					merchandise_doc = frappe.get_doc(
						"Event Attendee Ticket Merchandise",
						attendee.merchandise
					)

					for item in merchandise_doc.items:
						ticket.append("merchandise", {
							"merchandise_item": item.merchandise_item,
							"price": item.price,
							"quantity": item.quantity,
						})

				ticket.insert(ignore_permissions=True)
				ticket.submit()

			except Exception:
				frappe.log_error(
					frappe.get_traceback(),
					f"Failed creating ticket for {attendee.email}",
				)
				raise

