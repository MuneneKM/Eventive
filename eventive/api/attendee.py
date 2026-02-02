import frappe


@frappe.whitelist(allow_guest=True)
def get_all_events():
	"""
	Fetch all available events.
	
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
			"currency",
			"is_paid_event",
			"description",
			"organizer"
		],
		order_by="start_date asc",
		ignore_permissions=True
	)
	
	return events
