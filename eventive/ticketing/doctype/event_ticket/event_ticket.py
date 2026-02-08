# Copyright (c) 2026, Munene Morris and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EventTicket(Document):
	def after_insert(self):
		self.generate_qr_code()
	
	def generate_qr_code(self):
		import qrcode
		from io import BytesIO
		import frappe

		#QR code
		img = qrcode.make(self.name)
		buffer = BytesIO()
		img.save(buffer, format="PNG")
		buffer.seek(0)

		#creating file doc
		qr_file = frappe.get_doc({
			"doctype": "File",
			"file_name": f"EventTicket_{self.name}.png",
			"attached_to_doctype": "Event Ticket",
			"attached_to_name": self.name,
			"attached_to_field": "qr_code",
			"is_private": 1,
			"content": buffer.read(),
		})
		qr_file.insert()

		self.qr_code = qr_file.file_url
