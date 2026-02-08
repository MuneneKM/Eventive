# Copyright (c) 2026, Munene Morris and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class EventSession(Document):
	def validate(self):
		if not self.event or not self.start_date:
			return
		
		event = frappe.get_doc("Main Event", self.event)

		event_start = getdate(event.start_date)
		event_end = getdate(event.end_date)
		session_start = getdate(self.start_date)
		session_end = getdate(self.end_date)

		if session_start < event_start or session_end > event_end:
			frappe.throw("Session dates must be within the event dates")
