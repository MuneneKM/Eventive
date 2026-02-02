import frappe


@frappe.whitelist()
def get_by_event(event_id):
	"""
	Fetch all merchandise available for a specific event.
	
	Args:
	    event_id (str): The event ID
	
	Returns:
	    list: List of merchandise dictionaries containing item details
	"""
	merchandise_items = frappe.get_all(
		"Merchandise",
		filters={
			"event": event_id,
		},
		fields=[
			"name",
			"item_name",
			"description",
			"price",
			"currency",
			"item_image",
			"stock_quantity",
		],
		order_by="item_name asc",
		ignore_permissions=True
	)
	
	return merchandise_items
