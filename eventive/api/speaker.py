import frappe


@frappe.whitelist(allow_guest=True)
def get_all_speakers():
	"""
	Fetch all speakers.
	
	Returns:
	    list: List of speaker dictionaries containing speaker details
	"""
	speakers = frappe.get_all(
		"Speaker",
		fields=[
			"name",
			"full_name",
			"bio",
			"photo",
			"sessions",
			# "social_links" uncomment on fix
			"role",
			"company",
		],
		order_by="full_name asc",
		ignore_permissions=True
	)
	
	return speakers
