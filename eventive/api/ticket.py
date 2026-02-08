import frappe


@frappe.whitelist(allow_guest=True)
def get_registration(email, event_id):
	"""
	Fetch event registration details with attendees and tickets.
	
	Args:
	    email (str): The user's email address
	    event_id (str): The event ID
	
	Returns:
	    dict: Registration details with nested attendees and tickets
	"""
	# Get registration
	registrations = frappe.get_all(
		"Event Registration",
		filters={
			"email": email,
			"event": event_id
		},
		fields=["*"],
		ignore_permissions=True
	)
	
	if not registrations:
		return {
			"has_registration": False
		}
	
	registration = registrations[0]
	
	# Get event details
	event = frappe.get_doc("Main Event", event_id, ignore_permissions=True)
	
	response = {
		"has_registration": True,
		"registration_id": registration.name,
		"event_id": event_id,
		"event_name": event.event_name,
		"email": registration.email,
		"status": registration.status,
		"payment_status": registration.payment_status,
		"discount_code": registration.discount_code,
		"discount_amount": registration.discount_amount,
		"total_amount": registration.total_amount,
		"attendees": [],
		"tickets": []
	}
	
	# Get registration doc for nested table access
	registration_doc = frappe.get_doc("Event Registration", registration.name, ignore_permissions=True)
	
	# Process attendees with nested ticket and merchandise info
	for attendee in registration_doc.attendees:
		attendee_data = {
			"full_name": attendee.full_name,
			"email": attendee.email,
			"ticket_type": attendee.ticket_type,
			"ticket_price": attendee.ticket_price,
			"merchandise_total": attendee.merchandise_total,
			"merchandise": []
		}
		
		# Get merchandise details
		if attendee.merchandise:
			merchandise_doc = frappe.get_doc("Event Attendee Ticket Merchandise", attendee.merchandise, ignore_permissions=True)
			for item in merchandise_doc.items:
				attendee_data["merchandise"].append({
					"merchandise": item.merchandise_item,
					"quantity": item.quantity,
					"price": item.price
				})
		
		response["attendees"].append(attendee_data)
	
	# Get individual tickets for each attendee
	tickets = frappe.get_all(
		"Event Ticket",
		filters={
			"email": email
		},
		fields=["*"],
		ignore_permissions=True
	)
	
	for ticket in tickets:
		ticket_data = {
			"ticket_id": ticket.name,
			"event_id": ticket.event,
			"ticket_type": ticket.ticket_type,
			"email": ticket.email,
			"qr_code": ticket.qr_code,
			"issue_date": str(ticket.issue_date) if ticket.issue_date else None,
			"status": ticket.status,
			"checked_in": ticket.checked_in,
			"attendee": {}
		}
		
		# Find matching attendee info
		for attendee in registration_doc.attendees:
			if attendee.email == ticket.email:
				ticket_data["attendee"] = {
					"full_name": attendee.full_name,
					"email": attendee.email,
					"ticket_type": attendee.ticket_type,
					"ticket_price": attendee.ticket_price,
					"merchandise_total": attendee.merchandise_total,
					"merchandise": []
				}
				
				# Get merchandise for this attendee
				if attendee.merchandise:
					merchandise_doc = frappe.get_doc("Event Attendee Ticket Merchandise", attendee.merchandise, ignore_permissions=True)
					for item in merchandise_doc.items:
						ticket_data["attendee"]["merchandise"].append({
							"merchandise": item.merchandise_item,
							"quantity": item.quantity,
							"price": item.price
						})
				break
		
		response["tickets"].append(ticket_data)
	
	return response


@frappe.whitelist(allow_guest=True)
def get_ticket(email, event_id):
	"""
	Fetch ticket details with attendee, merchandise, and event information.
	
	Args:
	    email (str): The user's email address
	    event_id (str): The event ID
	
	Returns:
	    dict: Ticket details with all related information
	"""
	# Get ticket by email and event_id
	tickets = frappe.get_all(
		"Event Ticket",
		filters={
			"email": email,
			"event": event_id,
			"docstatus": 1
		},
		fields=["*"],
		ignore_permissions=True
	)
	
	if not tickets:
		return {
			"has_ticket": False
		}
	
	ticket = tickets[0]
	
	# Get event details
	event = frappe.get_doc("Main Event", ticket.event, ignore_permissions=True)
	
	# Get ticket type details
	ticket_type = frappe.get_doc("Ticket Type", ticket.ticket_type, ignore_permissions=True)
	
	response = {
		"has_ticket": True,
		"ticket_id": ticket.name,
		"event_id": ticket.event,
		"event_name": event.event_name,
		"start_date": str(event.start_date) if event.start_date else None,
		"end_date": str(event.end_date) if event.end_date else None,
		"venue": event.venue,
		"venue_name": event.venue_name,
		"ticket_type": ticket.ticket_type,
		"ticket_category": ticket_type.ticket_category,
		"ticket_category_name": ticket_type.ticket_category_name,
		"access_level": ticket_type.access_level,
		"ticket_price": ticket_type.ticket_price,
		"qr_code": ticket.qr_code,
		"issue_date": str(ticket.issue_date) if ticket.issue_date else None,
		"status": ticket.status,
		"checked_in": ticket.checked_in
	}
	
	# Get registration and attendee info
	if ticket.registration:
		registration = frappe.get_doc("Event Registration", ticket.registration, ignore_permissions=True)
		response["discount_code"] = registration.discount_code
		response["discount_amount"] = registration.discount_amount
		response["total_amount"] = registration.total_amount
		
		# Find the specific attendee in the registration
		for attendee in registration.attendees:
			if attendee.email == ticket.email:
				response["full_name"] = attendee.full_name
				response["email"] = attendee.email
				response["merchandise_total"] = attendee.merchandise_total
				
				# Get merchandise details
				if attendee.merchandise:
					merchandise_doc = frappe.get_doc("Event Attendee Ticket Merchandise", attendee.merchandise, ignore_permissions=True)
					response["merchandise"] = []
					for item in merchandise_doc.items:
						response["merchandise"].append({
							"merchandise": item.merchandise_item,
							"quantity": item.quantity,
							"price": item.price
						})
				break
	
	return response


@frappe.whitelist(allow_guest=True)
def get_ticket_types(event_id):
	"""
	Fetch all ticket types for a specific event.
	
	Args:
	    event_id (str): The event ID
	
	Returns:
	    list: List of ticket type dictionaries
	"""
	ticket_types = frappe.get_all(
		"Ticket Type",
		filters={
			"event": event_id
		},
		fields=[
			"name",
			"ticket_category",
			"ticket_category_name",
			"ticket_price",
			"access_level",
			"sales_start",
			"sales_end"
		],
		order_by="ticket_price asc",
		ignore_permissions=True
	)
	
	# Convert datetime fields to string for JSON serialization
	for ticket_type in ticket_types:
		if ticket_type.sales_start:
			ticket_type.sales_start = str(ticket_type.sales_start)
		if ticket_type.sales_end:
			ticket_type.sales_end = str(ticket_type.sales_end)
	
	return ticket_types


@frappe.whitelist(allow_guest=True)
def has_ticket(email, event_id):
	"""
	Check if a user has a ticket for a specific event.
	
	Args:
	    email (str): The user's email address
	    event_id (str): The event ID
	
	Returns:
	    dict: Ticket status with details
	"""
	ticket = frappe.get_all(
		"Event Ticket",
		filters={
			"email": email,
			"event": event_id,
			# "docstatus": 1,
			"status": "Valid"
		},
		fields=[
			"name",
			"ticket_type",
			"status",
			"checked_in"
		],
		ignore_permissions=True
	)
	
	if ticket:
		return {
			"has_ticket": True,
			"ticket": ticket[0]
		}
	
	return {
		"has_ticket": False
	}


@frappe.whitelist()
def get_my_tickets(email=None):
	"""
	Fetch all tickets for the current user.
	
	Returns:
	    list: List of ticket dictionaries containing ticket details
	"""
	if not email:
		email = frappe.session.user

	if not email or email == "Guest":
		frappe.throw("Please login to view your tickets", frappe.PermissionError)

	tickets = frappe.get_all(
		"Event Ticket",
		filters={
			"email": email,
			"docstatus": 1
		},
		fields=[
			"name",
			"ticket_type",
			"event",
			"registration",
			"qr_code",
			"issue_date",
			"status",
			"merchandise"
		],
		order_by="issue_date desc",
		ignore_permissions=True
	)
	
	# Get event names for each ticket
	for ticket in tickets:
		event = frappe.get_doc("Main Event", ticket.event, ignore_permissions=True)
		ticket.event_name = event.event_name
		ticket.start_date = event.start_date
		ticket.end_date = event.end_date
	
	return tickets


@frappe.whitelist()
def download_ticket(ticket_id):
	"""
	Get ticket details for download.
	
	Args:
	    ticket_id (str): The ticket ID
	
	Returns:
	    dict: Ticket details with QR code URL
	"""
	if not frappe.session.user or frappe.session.user == "Guest":
		frappe.throw("Please login to download your ticket", frappe.PermissionError)
	
	ticket = frappe.get_doc("Event Ticket", ticket_id, ignore_permissions=True)
	
	# Check if user owns this ticket
	if ticket.email != frappe.session.user:
		frappe.throw("You don't have permission to access this ticket", frappe.PermissionError)
	
	event = frappe.get_doc("Main Event", ticket.event, ignore_permissions=True)
	
	return {
		"ticket_id": ticket.name,
		"ticket_type": ticket.ticket_type,
		"event_name": event.event_name,
		"event_start_date": event.start_date,
		"event_end_date": event.end_date,
		"event_venue": event.venue,
		"qr_code": ticket.qr_code,
		"issue_date": ticket.issue_date,
		"status": ticket.status
	}
