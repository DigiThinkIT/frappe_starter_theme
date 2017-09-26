from __future__ import unicode_literals
import re
import frappe
import json
import urllib
from datetime import datetime
from frappe.website.utils import get_shade
from frappe.website.doctype.website_theme.website_theme import get_active_theme

no_sitemap = 1
base_template_path = "templates/www/starter_theme.css"

default_properties = {
	"background_color": "#000000",
	"top_bar_color": "#ffffff",
	"top_bar_text_color": "#000000",
	"footer_color": "#ffffff",
	"footer_text_color": "#000000",
	"font_size": "14px",
	"text_color": "#000000",
	"link_color": "#000000"
}

def json_default(obj):

	if isinstance(obj, datetime):
		return obj.isoformat()

	if hasattr(obj, "__dict__"):
		return str(obj) # copy.copy(obj.__dict__) #removed due to circular reference

	raise TypeError("Unserializable object {} of type {}".format(obj, type(obj)))

def get_context(context):
	"""returns web style"""
	website_theme = get_active_theme()
	if not website_theme:
		return {}

	path_name = context.get("pathname", "")

	if path_name[0:11] == "theme/page/":

		page_name = path_name[11:-4]
		if page_name and frappe.db.exists("Web Page", page_name):
			page = frappe.get_doc("Web Page", page_name)

			if page and page.get("theme_override", None):
				if frappe.db.exists("Website Theme", page.get("theme_override")):
					override_theme = frappe.get_doc("Website Theme", page.get("theme_override"))
					if page.theme_override_mode == "Inherit":
						ignore_keys = ["owner", "modified_by", "creation", "docstatus", "modified"]
						for key in override_theme.as_dict().keys():
							if key not in ignore_keys:
								website_theme.set(key, override_theme.get(key))

					elif page.theme_override_mode == "Full":
						website_theme = override_theme

	prepare(website_theme)

	context["theme"] = website_theme

	return context

def prepare(theme):
	for d in default_properties:
		if not theme.get(d):
			theme.set(d, default_properties[d])

	theme.footer_border_color = get_shade(theme.footer_color, 10)
	theme.border_color = get_shade(theme.background_color, 10)

	webfonts = list(set(theme.get(key)
		for key in ("heading_webfont", 'text_webfont') if theme.get(key)))

	theme.webfont_import = "\n".join('@import url(https://fonts.googleapis.com/css?family={0}:400,300,400italic,700&subset=latin,latin-ext);'\
		.format(font.replace(" ", "+")) for font in webfonts)

	# move @import from css field to the top of the css file
	if theme.css:
		if "@import url" in theme.css:
			webfont_import = list(set(re.findall("@import url\([^\(\)]*\);", theme.css)))
			theme.webfont_import += "\n" + "\n".join(webfont_import)
			for wfimport in webfont_import:
				theme.css = theme.css.replace(wfimport, "")
