from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.password import update_password

@frappe.whitelist(allow_guest=True)
def sign_up(email, first_name, last_name, pwd=None, redirect_to=None):
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
			"first_name": first_name,
			"last_name": last_name,
			"enabled": 1,
			"user_type": "Website User",
			"send_welcome_email": True
		})

		if pwd:
			user.send_welcome_email = False
		
		user.flags.ignore_permissions = True
		user.insert()
		
		if pwd:
			update_password(user.name, pwd)
			frappe.local.login_manager.login_as(email)
			frappe.set_user(email)

		if redirect_to:
			frappe.cache().hset('redirect_after_login', user.name, redirect_to)

		if user.flags.email_sent:
			return _("Please check your email for verification")
		else:
			return _("Please ask your administrator to verify your sign-up")
