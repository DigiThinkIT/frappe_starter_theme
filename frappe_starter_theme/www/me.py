# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.user import get_fullname_and_avatar
import frappe.www.list

no_cache = 1
no_sitemap = 1

def get_context(context):
	from awesome_cart.compat.customer import get_current_customer
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)

	context.show_sidebar=True

	customer = get_current_customer()

	context["total_unpaid"] = frappe.db.sql("""select sum(outstanding_amount)
	from `tabSales Invoice`
	where customer=%s and docstatus = 1""", customer.name)[0][0] or ""

	context["credit_limit"] = customer.credit_limit
	context["credit_days_based_on"] = customer.credit_days_based_on
	context["credit_days"] = customer.credit_days
	
	return context