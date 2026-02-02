# Copyright (c) 2026, Munene Morris and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EventRegistrationAttendee(Document):

	def get_merchandise_total(self):
		if not self.merchandise:
			return 0

		merchandise = frappe.get_cached_doc("Event Attendee Ticket Merchandise", self.merchandise)
		total = sum((item.price * item.quantity) for item in merchandise.items)
		self.merchandise_total = total
		return total

	def after_insert(self):
		self.check_ticket_included_merchandise()
		self.update_merchandise_total()

	def check_ticket_included_merchandise(self):
		if not self.ticket_type:
			return

		ticket_type = frappe.get_doc("Ticket Type", self.ticket_type)

		if ticket_type.includes_merchandise and ticket_type.included_merchandise:
			# Only set if not already set
			if self.merchandise != ticket_type.included_merchandise:
				self.db_set("merchandise", ticket_type.included_merchandise)

	def update_merchandise_total(self):
		if not self.merchandise:
			self.db_set("merchandise_total", 0)
			return 0

		merchandise = frappe.get_doc(
			"Event Attendee Ticket Merchandise",
			self.merchandise
		)

		total = sum(
			(item.price or 0) * (item.quantity or 0)
			for item in merchandise.items
		)

		self.db_set("merchandise_total", total)
		return total
