import frappe


@frappe.whitelist(allow_guest=True)
def create_booking(event_id, email, discount_code=None, attendees=None):
	"""
	Create a booking for an event.
	
	Args:
	    event_id (str): The event ID
	    email (str): The booker's email
	    discount_code (str): Optional discount code
	    attendees (list): List of attendee dictionaries
	
	Returns:
	    dict: Booking result with registration ID and ticket IDs
	"""
	if not attendees:
		frappe.throw("At least one attendee is required", frappe.ValidationError)
	
	# Parse attendees if it's a JSON string
	if isinstance(attendees, str):
		attendees = frappe.parse_json(attendees)
	
	# Calculate total amount
	total_amount = sum(attendee.get("total_amount", 0) for attendee in attendees)
	
	# Create Event Registration
	registration = frappe.get_doc({
		"doctype": "Event Registration",
		"event": event_id,
		"email": email,
		"discount_code": discount_code,
		"status": "Pending",
		"payment_status": "Unpaid",
	})
	
	# Add attendees
	for attendee_data in attendees:
		attendee_row = {
			"full_name": attendee_data.get("full_name"),
			"email": attendee_data.get("email"),
			"ticket_type": attendee_data.get("ticket_type"),
			"ticket_price": attendee_data.get("ticket_price", 0),
			"merchandise_total": attendee_data.get("merchandise_total", 0)
		}
		
		# Create merchandise document if attendee has merchandise
		merchandise = attendee_data.get("merchandise")
		if merchandise:
			merchandise_doc = frappe.get_doc({
				"doctype": "Event Attendee Ticket Merchandise"
			})
			
			for item in merchandise:
				merchandise_doc.append("items", {
					"merchandise_item": item.get("merchandise"),
					"quantity": item.get("quantity", 1)
				})
			
			merchandise_doc.insert(ignore_permissions=True)
			attendee_row["merchandise"] = merchandise_doc.name
		
		registration.append("attendees", attendee_row)
	
	registration.insert(ignore_permissions=True)
	
	# Get created tickets
	tickets = frappe.get_all(
		"Event Ticket",
		filters={
			"registration": registration.name
		},
		fields=["name", "email", "ticket_type"],
		ignore_permissions=True
	)
	
	return {
		"registration_id": registration.name,
		"tickets": tickets,
		"total_amount": total_amount,
		"status": "Booking created successfully"
	}
