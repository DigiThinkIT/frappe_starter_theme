from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import cint, has_gravatar, format_datetime, now_datetime, get_formatted_email
from frappe import throw, msgprint, _
from frappe.utils.password import update_password as _update_password
from frappe.desk.notifications import clear_notifications
from frappe.utils.user import get_system_managers
import frappe.permissions
import frappe.share
import re
from frappe.limits import get_limits

@frappe.whitelist(allow_guest=True)
def sign_up(email, full_name, pwd=None, redirect_to=None):
	user = frappe.db.get("User", {"email": email})
	if user:
		if user.disabled:
			return _("Registered but disabled.")
		else:
			return _("Already Registered")
	else:
		if frappe.db.sql("""select count(*) from tabUser where
			HOUR(TIMEDIFF(CURRENT_TIMESTAMP, TIMESTAMP(modified)))=1""")[0][0] > 300:

			frappe.respond_as_web_page(_('Temperorily Disabled'),
				_('Too many users signed up recently, so the registration is disabled. Please try back in an hour'),
				http_status_code=429)

		user = frappe.get_doc({
			"doctype":"User",
			"email": email,
			"first_name": full_name,
			"enabled": 1,
			"user_type": "Website User",
			"send_welcome_email": True
		})

		if pwd:
			user.new_password = pwd
			user.send_welcome_email = False
		
		user.flags.ignore_permissions = True
		user.insert()
		
		if pwd:
			frappe.local.login_manager.login_as(email)
			frappe.set_user(email)

		if redirect_to:
			frappe.cache().hset('redirect_after_login', user.name, redirect_to)

		if user.flags.email_sent:
			return _("Please check your email for verification")
		else:
			return _("Please ask your administrator to verify your sign-up")
