import frappe


@frappe.whitelist()
def get_by_event(event_id):
	"""
	Fetch all sessions for a specific event.
	
	Args:
	    event_id (str): The event ID
	
	Returns:
	    list: List of session dictionaries containing session details
	"""
	sessions = frappe.get_all(
		"Event Session",
		filters={
			"event": event_id,
		},
		fields=[
			"name",
			"session_title",
			"description",
			"start_time",
			"end_time",
			"track",
			"session_type",
			"capacity",
			"talk_name",
			"allow_booking",
			"is_booked",
			"booked_spots"
		],
		order_by="start_time asc",
		ignore_permissions=True
	)
	
	# Convert time fields to string for JSON serialization
	for session in sessions:
		if session.start_time:
			session.start_time = str(session.start_time)
		if session.end_time:
			session.end_time = str(session.end_time)
	
	return sessions
