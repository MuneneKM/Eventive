import frappe


@frappe.whitelist()
def get_matches(event_id=None):
	"""
	Fetch networking matches for the current user.
	
	Args:
	    event_id (str): Optional event ID to filter matches
	
	Returns:
	    list: List of match dictionaries with attendee details
	"""
	if not frappe.session.user or frappe.session.user == "Guest":
		frappe.throw("Please login to view networking matches", frappe.PermissionError)
	
	# Get current user's attendee profile
	current_user_profile = frappe.get_all(
		"Attendee Profile",
		filters={"user": frappe.session.user},
		fields=["name", "open_to_networking"],
		limit=1,
		ignore_permissions=True
	)
	
	if not current_user_profile:
		return []
	
	current_profile = current_user_profile[0]
	
	# Check if current user is open to networking
	if not current_profile.get("open_to_networking"):
		return []
	
	filters = {
		"status": "Suggested",
	}
	
	if event_id:
		filters["event"] = event_id
	
	matches = frappe.get_all(
		"Match Suggestion",
		filters=filters,
		fields=[
			"name",
			"attendee_1",
			"attendee_2",
			"event",
			"match_score",
			"status"
		],
		order_by="match_score desc",
		ignore_permissions=True
	)
	
	# Get attendee profile details for each match
	result = []
	for match in matches:
		# Only process if current user is attendee_1 or attendee_2
		if match.attendee_1 != current_profile.name and match.attendee_2 != current_profile.name:
			continue
		
		# Determine the other attendee
		other_attendee = match.attendee_2 if match.attendee_1 == current_profile.name else match.attendee_1
		
		# Get the matched user's profile
		attendee_profile = frappe.get_all(
			"Attendee Profile",
			filters={"name": other_attendee},
			fields=["name", "user", "full_name", "company", "job_title", "bio", "profile_image", "social_link", "open_to_networking", "interests"],
			limit=1,
			ignore_permissions=True
		)
		
		if not attendee_profile:
			continue
		
		profile = attendee_profile[0]
		
		# Check if the other attendee is open to networking
		if not profile.get("open_to_networking"):
			continue
		
		# Get interests for the matched user
		interests = frappe.get_all(
			"Interest Tags",
			filters={"parent": profile.name},
			fields=["tag"],
			ignore_permissions=True
		)
		
		# Build nested profile object
		nested_profile = {
			"name": profile.name,
			"user": profile.user,
			"full_name": profile.full_name,
			"company": profile.company,
			"job_title": profile.job_title,
			"bio": profile.bio,
			"profile_image": profile.profile_image,
			"social_link": profile.social_link,
			"open_to_networking": profile.open_to_networking,
			"interests": [{"tag": i.tag} for i in interests]
		}
		
		result.append({
			"match_id": match.name,
			"attendee_2": nested_profile,
			"match_score": match.match_score,
			"event": match.event,
			"status": match.status
		})
	
	return result

@frappe.whitelist()
def get_connected_matches(event_id=None):
	"""
	Fetch connected networking matches for the current user.
	
	Args:
	    event_id (str): Optional event ID to filter matches
	
	Returns:
	    list: List of connected match dictionaries with attendee details
	"""
	if not frappe.session.user or frappe.session.user == "Guest":
		frappe.throw("Please login to view networking matches", frappe.PermissionError)
	
	# Get current user's attendee profile
	current_user_profile = frappe.get_all(
		"Attendee Profile",
		filters={"user": frappe.session.user},
		fields=["name", "open_to_networking"],
		limit=1,
		ignore_permissions=True
	)
	
	if not current_user_profile:
		return []
	
	current_profile = current_user_profile[0]
	
	# Check if current user is open to networking
	if not current_profile.get("open_to_networking"):
		return []
	
	filters = {
		"status": "Connected",
	}
	
	if event_id:
		filters["event"] = event_id
	
	matches = frappe.get_all(
		"Match Suggestion",
		filters=filters,
		fields=[
			"name",
			"attendee_1",
			"attendee_2",
			"event",
			"match_score",
			"status"
		],
		order_by="creation desc",
		ignore_permissions=True
	)
	
	# Get attendee profile details for each match
	result = []
	for match in matches:
		# Only process if current user is attendee_1 or attendee_2
		if match.attendee_1 != current_profile.name and match.attendee_2 != current_profile.name:
			continue
		
		# Determine the other attendee
		other_attendee = match.attendee_2 if match.attendee_1 == current_profile.name else match.attendee_1
		
		# Get the matched user's profile
		attendee_profile = frappe.get_all(
			"Attendee Profile",
			filters={"name": other_attendee},
			fields=["name", "user", "full_name", "company", "job_title", "bio", "profile_image", "social_link", "open_to_networking"],
			limit=1,
			ignore_permissions=True
		)
		
		if not attendee_profile:
			continue
		
		profile = attendee_profile[0]
		
		# Check if the other attendee is open to networking
		if not profile.get("open_to_networking"):
			continue
		
		# Get interests for the matched user
		# interests = frappe.get_all(
		# 	"Interest Tags",
		# 	filters={"parent": profile.name},
		# 	fields=["interest"],
		# 	ignore_permissions=True
		# )
		
		# Build nested profile object
		nested_profile = {
			"name": profile.name,
			"user": profile.user,
			"full_name": profile.full_name,
			"company": profile.company,
			"job_title": profile.job_title,
			"bio": profile.bio,
			"profile_image": profile.profile_image,
			"social_link": profile.social_link,
			"open_to_networking": profile.open_to_networking,
			# "interests": [{"tag": i.interest} for i in interests]
		}
		
		result.append({
			"match_id": match.name,
			"attendee_2": nested_profile,
			"match_score": match.match_score,
			"event": match.event,
			"status": match.status,
			"connected_on": match.modified
		})
	
	return result


@frappe.whitelist()
def send_message(receiver_id=None, event_id=None, message=None):
	"""
	Send a networking message to another attendee.
	
	Args:
	    receiver_id (str): User ID of the message recipient
	    event_id (str): Event ID for the message
	    message (str): Message content
	
	Returns:
	    dict: Created message details
	"""
	if not frappe.session.user or frappe.session.user == "Guest":
		frappe.throw("Please login to send messages", frappe.PermissionError)
	
	if not receiver_id or not message:
		frappe.throw("Missing required fields: receiver_id and message are required")

	# Get sender's attendee profile
	sender_profile = frappe.get_all(
		"Attendee Profile",
		filters={"user": frappe.session.user},
		fields=["name", "full_name"],
		limit=1,
		ignore_permissions=True
	)
	
	if not sender_profile:
		frappe.throw("You must have an attendee profile to send messages")
	
	sender_name = sender_profile[0].full_name or frappe.session.user
	
	# Get receiver's name
	receiver_name = frappe.get_value("User", receiver_id, "full_name") or receiver_id
	
	# Create the Networking Message
	msg = frappe.get_doc({
		"doctype": "Networking Message",
		"sender": frappe.session.user,
		"receiver": receiver_id,
		"sender_name": sender_name,
		"receiver_name": receiver_name,
		"message": message,
		"is_read": 0
	})
	msg.insert(ignore_permissions=True)
	
	return {
		"message_id": msg.name,
		"sender": frappe.session.user,
		"receiver": receiver_id,
		"message": message,
		"created_on": msg.creation
	}


@frappe.whitelist()
def get_messages(other_user_id=None, event_id=None):
	"""
	Get networking messages between current user and another user for an event.
	
	Args:
	    other_user_id (str): User ID of the other participant
	    event_id (str): Event ID to filter messages
	
	Returns:
	    list: List of message dictionaries
	"""
	if not frappe.session.user or frappe.session.user == "Guest":
		frappe.throw("Please login to view messages", frappe.PermissionError)
	
	if not other_user_id or not event_id:
		frappe.throw("Missing required fields: other_user_id and event_id are required")
	
	# Get messages where current user is sender or receiver, and other_user_id is the other party
	messages = frappe.get_all(
		"Networking Message",
		filters=[
			["Networking Message", "event", "=", event_id],
			["Networking Message", "sender", "in", [frappe.session.user, other_user_id]],
			["Networking Message", "receiver", "in", [frappe.session.user, other_user_id]]
		],
		fields=[
			"name",
			"sender",
			"receiver",
			"sender_name",
			"receiver_name",
			"message",
			"is_read",
			"creation"
		],
		order_by="creation asc",
		ignore_permissions=True
	)
	
	result = []
	for msg in messages:
		result.append({
			"id": msg.name,
			"sender_id": msg.sender,
			"receiver_id": msg.receiver,
			"sender_name": msg.sender_name,
			"receiver_name": msg.receiver_name,
			"message": msg.message,
			"is_read": bool(msg.is_read),
			"created_at": msg.creation
		})
	
	return result
