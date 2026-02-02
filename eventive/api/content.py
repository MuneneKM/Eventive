import frappe


@frappe.whitelist()
def get_by_event(event_id):
	"""
	Fetch all digital content available for a specific event.
	
	Args:
	    event_id (str): The event ID
	
	Returns:
	    list: List of content dictionaries containing content details
	"""
	content_items = frappe.get_all(
		"Digital Content",
		filters={
			"event": event_id,
		},
		fields=[
			"name",
			"title",
			"content_type",
			"thumbnail",
			"session",
			"access_level",
			"description",
			"file",
			"publish_date",
			# "content_tags"
		],
		order_by="publish_date desc",
		ignore_permissions=True
	)
	
	return content_items


