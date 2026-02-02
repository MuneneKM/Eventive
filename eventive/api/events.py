import frappe


@frappe.whitelist(allow_guest=True)
def get_sponsor_tiers(event_id):
	"""
	Fetch all sponsor tiers for an event.
	
	Args:
	    event_id (str): The event ID
	
	Returns:
	    list: List of sponsor tier dictionaries
	"""
	sponsor_tiers = frappe.get_all(
		"Sponsor Tier",
		filters={
			"event": event_id
		},
		fields=[
			"name",
			"tier_name",
			"amount",
			"currency",
			"description"
		],
		order_by="amount asc",
		ignore_permissions=True
	)
	
	return sponsor_tiers


@frappe.whitelist(allow_guest=True)
def get_booth_packages(event_id):
	"""
	Fetch all booth packages for an event.
	
	Args:
	    event_id (str): The event ID
	
	Returns:
	    list: List of booth package dictionaries
	"""
	booth_packages = frappe.get_all(
		"Booth Package",
		filters={
			"event": event_id
		},
		fields=[
			"name",
			"package_name",
			"booth_size",
			"price",
			"currency",
			"available_booths",
			"includes_passes",
			"includes_power",
			"includes_internet"
		],
		order_by="price asc",
		ignore_permissions=True
	)
	
	return booth_packages


@frappe.whitelist(allow_guest=True)
def create_exhibitor(exhibitor_name, email, phone, logo=None, website=None, event=None, booth_package=None, notes=None):
	"""
	Create a new exhibitor.
	
	Args:
	    exhibitor_name (str): Exhibitor name
	    email (str): Email address
	    phone (str): Phone number
	    logo (str): Logo image URL
	    website (str): Website URL
	    event (str): Event ID
	    booth_package (str): Booth Package ID
	    notes (str): Additional notes
	
	Returns:
	    dict: Created exhibitor details
	"""
	exhibitor = frappe.get_doc({
		"doctype": "Exhibitor",
		"exhibitor_name": exhibitor_name,
		"email": email,
		"phone": phone,
		"logo": logo,
		"website": website,
		"event": event,
		"booth_package": booth_package,
		"notes": notes,
		"status": "Draft"
	})
	
	exhibitor.insert(ignore_permissions=True)
	
	return {
		"exhibitor_id": exhibitor.name,
		"status": "Created",
		"message": "Exhibitor registration submitted successfully"
	}


@frappe.whitelist(allow_guest=True)
def create_sponsor(sponsor_name, tier, event=None, company=None, company_logo=None):
	"""
	Create a new sponsor.
	
	Args:
	    sponsor_name (str): Sponsor name
	    tier (str): Sponsor Tier ID
	    event (str): Event ID
	    company (str): Company name
	    company_logo (str): Company logo URL
	
	Returns:
	    dict: Created sponsor details
	"""
	# Get tier details for tier_name and amount
	tier_doc = frappe.get_doc("Sponsor Tier", tier, ignore_permissions=True)
	
	sponsor = frappe.get_doc({
		"doctype": "Sponsor",
		"sponsor_name": sponsor_name,
		"tier": tier,
		"event": event or tier_doc.event,
		"company": company,
		"company_logo": company_logo
	})
	
	sponsor.insert(ignore_permissions=True)
	
	return {
		"sponsor_id": sponsor.name,
		"tier_name": tier_doc.tier_name,
		"amount": tier_doc.amount,
		"status": "Created",
		"message": "Sponsor registration submitted successfully"
	}


@frappe.whitelist()
def get_all():
	"""
	Fetch all published events.
	
	Returns:
	    list: List of event dictionaries containing event details
	"""
	events = frappe.get_all(
		"Main Event",
		filters={
			"is_published": 1,
		},
		fields=[
			"name",
			"event_name",
			"banner_image",
			"start_date",
			"end_date",
			"status",
			"capacity",
			"venue",
			"venue_name",
			"currency",
			"is_paid_event",
			"description",
			"organizer",
			"host_name",
			"allow_networking",
			"allow_digital_content"
		],
		order_by="start_date asc",
		ignore_permissions=True
	)
	
	return events


@frappe.whitelist()
def get_by_id(event_id):
	"""
	Fetch event details by ID.
	
	Args:
	    event_id (str): The name/ID of the event
	
	Returns:
	    dict: Event details
	"""
	event = frappe.get_doc("Main Event", event_id, ignore_permissions=True)
	
	return {
		"name": event.name,
		"event_name": event.event_name,
		"banner_image": event.banner_image,
		"start_date": event.start_date,
		"end_date": event.end_date,
		"status": event.status,
		"capacity": event.capacity,
		"venue": event.venue,
		"venue_name": event.venue_name,
		"currency": event.currency,
		"is_paid_event": event.is_paid_event,
		"description": event.description,
		"host_name": event.host_name,
		"organizer": event.organizer,
		"allow_networking": event.allow_networking,
		"allow_digital_content": event.allow_digital_content,
		"is_published": event.is_published
	}


@frappe.whitelist()
def get_my_events():
	"""
	Fetch events that the current user has registered for.
	
	Returns:
	    list: List of event dictionaries containing event details
	"""
	if not frappe.session.user or frappe.session.user == "Guest":
		frappe.throw("Please login to view your events", frappe.PermissionError)
	
	# Get registrations for current user
	registrations = frappe.get_all(
		"Event Registration",
		filters={
			"email": frappe.session.user_id,
			"docstatus": 1
		},
		fields=["event"],
		ignore_permissions=True
	)
	
	if not registrations:
		return []
	
	event_ids = list(set([r.event for r in registrations]))
	
	events = frappe.get_all(
		"Main Event",
		filters={
			"name": ["in", event_ids]
		},
		fields=[
			"name",
			"event_name",
			"banner_image",
			"start_date",
			"end_date",
			"status",
			"capacity",
			"venue",
			"currency",
			"is_paid_event",
			"description",
			"organizer",
			"allow_networking",
			"allow_digital_content"
		],
		order_by="start_date asc",
		ignore_permissions=True
	)
	
	return events


@frappe.whitelist()
def register_for_event(event, attendees=None):
	"""
	Register for an event.
	
	Args:
	    event (str): The event ID
	    attendees (list): List of attendee dictionaries with email, name, ticket_type
	
	Returns:
	    dict: Registration details
	"""
	if not frappe.session.user or frappe.session.user == "Guest":
		frappe.throw("Please login to register for events", frappe.PermissionError)
	
	event_doc = frappe.get_doc("Main Event", event, ignore_permissions=True)
	
	if not event_doc.is_published:
		frappe.throw("This event is not open for registration")
	
	# Check capacity
	existing_registrations = frappe.get_all(
		"Event Registration",
		filters={
			"event": event,
			"docstatus": 1
		},
		fields=["name"],
		ignore_permissions=True
	)
	
	if event_doc.capacity and len(existing_registrations) >= event_doc.capacity:
		frappe.throw("This event is fully booked")
	
	registration = frappe.get_doc({
		"doctype": "Event Registration",
		"event": event,
		"user": frappe.session.user,
	})
	
	# Add attendees if provided
	if attendees:
		import json
		if isinstance(attendees, str):
			attendees = json.loads(attendees)
		
		for attendee in attendees:
			registration.append("attendees", {
				"email": attendee.get("email"),
				"attendee_name": attendee.get("name"),
				"ticket_type": attendee.get("ticket_type"),
				"ticket_price": attendee.get("ticket_price", 0)
			})
	
	registration.insert(ignore_permissions=True)
	registration.submit()
	
	return {
		"registration_id": registration.name,
		"event": event,
		"status": "Registered",
		"message": "Successfully registered for the event"
	}


@frappe.whitelist()
def submit_feedback(event, rating, feedback=None):
	"""
	Submit feedback for an event.
	
	Args:
	    event (str): The event ID
	    rating (int): Rating (1-5)
	    feedback (str): Optional feedback text
	
	Returns:
	    dict: Feedback submission result
	"""
	if not frappe.session.user or frappe.session.user == "Guest":
		frappe.throw("Please login to submit feedback", frappe.PermissionError)
	
	if not rating or rating < 1 or rating > 5:
		frappe.throw("Rating must be between 1 and 5")
	
	feedback_doc = frappe.get_doc({
		"doctype": "Event Feedback",
		"event": event,
		"user": frappe.session.user,
		"rating": rating,
		"feedback": feedback
	})
	
	feedback_doc.insert(ignore_permissions=True)
	
	return {
		"feedback_id": feedback_doc.name,
		"status": "Submitted",
		"message": "Thank you for your feedback"
	}
