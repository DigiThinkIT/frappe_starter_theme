from __future__ import unicode_literals
import frappe
from frappe.website.doctype.website_theme.website_theme import get_active_theme

def get_starter_theme_context(context):
	theme = get_active_theme()
	if not frappe.local.conf.get("website_context"):
		frappe.local.conf["website_context"] = {}

	theme_values = {}
	for fieldname in theme.__dict__.keys():
		if fieldname.startswith("theme_"):
			theme_values[fieldname] = theme.get(fieldname)

	frappe.local.conf['website_context'].update(theme_values)
	
