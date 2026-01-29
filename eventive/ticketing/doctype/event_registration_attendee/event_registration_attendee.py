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
