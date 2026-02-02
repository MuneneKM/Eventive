import frappe
from frappe.utils.password import update_password


@frappe.whitelist(allow_guest=True)
def api_login(email, password):
    try:
        lm = frappe.local.login_manager
        lm.authenticate(user=email, pwd=password)
        lm.post_login()
    except frappe.AuthenticationError:
        frappe.clear_messages()
        frappe.throw("Invalid email or password", frappe.AuthenticationError)

    return {
        "user_id": frappe.session.user,
        "email": frappe.session.user,
        "message": "Login successful"
    }


@frappe.whitelist()
def api_logout():
	"""
	Logout the current user.
	
	Returns:
	    dict: Logout status
	"""
	frappe.local.login_manager.logout()
	
	return {
		"message": "Logged out successfully"
	}


@frappe.whitelist()
def get_current_user():
	"""
	Get the current logged-in user details.
	
	Returns:
	    dict: User details
	"""
	if not frappe.session.user or frappe.session.user == "Guest":
		return {
			"user_id": None,
			"email": None,
			"is_logged_in": False
		}
	
	user = frappe.get_doc("User", frappe.session.user, ignore_permissions=True)
	
	return {
		"user_id": user.name,
		"email": user.email,
		"full_name": user.full_name,
		"first_name": user.first_name,
		"last_name": user.last_name,
		"is_logged_in": True
	}


@frappe.whitelist()
def get_current_attendee():
	"""
	Get the current logged-in attendee details, combining User and Attendee Profile data.
	
	Returns:
	    dict: Attendee details including user and profile information
	"""
	if not frappe.session.user or frappe.session.user == "Guest":
		return {
			"user_id": None,
			"email": None,
			"is_logged_in": False
		}
	
	user = frappe.get_doc("User", frappe.session.user, ignore_permissions=True)
	
	# Get attendee profile for the current user
	attendee_profiles = frappe.get_all(
		"Attendee Profile",
		filters={
			"user": frappe.session.user
		},
		fields=["*"],
		ignore_permissions=True
	)
	
	attendee_data = {
		"user_id": user.name,
		"email": user.email,
		"first_name": user.first_name,
		"last_name": user.last_name,
		"full_name": user.full_name,
		"is_logged_in": True,
		"profiles": []
	}
	
	# Add attendee profile data to each profile
	for profile in attendee_profiles:
		profile_data = {
			"profile_id": profile.name,
			"full_name": profile.full_name,
			"profile_image": profile.profile_image,
			"event": profile.event,
			"role": profile.role,
			"open_to_networking": profile.open_to_networking,
			"social_link": profile.social_link,
			"company": profile.company,
			"job_title": profile.job_title,
			"bio": profile.bio
		}
		
		# Get interests for this profile
		interests = frappe.get_all(
			"Interest Tags",
			filters={
				"parent": profile.name
			},
			fields=["interest"],
			ignore_permissions=True
		)
		profile_data["interests"] = [i.interest for i in interests]
		
		attendee_data["profiles"].append(profile_data)
	
	return attendee_data


@frappe.whitelist(allow_guest=True)
def register(email, password, first_name=None, full_name=None, profile_image=None, role="Attendee", open_to_networking=0, social_link=None, company=None, job_title=None, bio=None, interests=None):
	if frappe.db.exists("User", email):
		frappe.throw("User already exists")

	user = frappe.get_doc({
		"doctype": "User",
		"email": email,
		"role_profile": "Attendee",
		"first_name": first_name or full_name or email,
		"full_name": full_name or first_name or email,
		"enabled": 1
	})
	user.insert(ignore_permissions=True)
	update_password(user.name, password)

	# Create attendee profile
	attendee_profile = frappe.get_doc({
		"doctype": "Attendee Profile",
		"user": user.name,
		"full_name": full_name,
		"profile_image": profile_image,
		"role": "Attendee",
		"open_to_networking": open_to_networking,
		"social_link": social_link,
		"company": company,
		"job_title": job_title,
		"bio": bio
	})
	
	# Handle interests if provided
	if interests:
		if isinstance(interests, str):
			interests = frappe.parse_json(interests)
		for interest in interests:
			attendee_profile.append("interests", {
				"interest": interest
			})
	
	attendee_profile.insert(ignore_permissions=True)

	return {
		"user_id": user.name,
		"email": user.email,
		"attendee_profile_id": attendee_profile.name
	}
