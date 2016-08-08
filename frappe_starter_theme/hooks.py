# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "frappe_starter_theme"
app_title = "Frappe Starter Theme"
app_publisher = "DigiThinkIT, Inc."
app_description = "A modular and extensible frappe theme"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "forellana@digithinkit.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/frappe_starter_theme/css/frappe_starter_theme.css"
# app_include_js = "/assets/frappe_starter_theme/js/frappe_starter_theme.js"

# include js, css files in header of web template
# web_include_css = "/assets/frappe_starter_theme/css/frappe_starter_theme.css"
# web_include_js = "/assets/frappe_starter_theme/js/frappe_starter_theme.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "frappe_starter_theme.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "frappe_starter_theme.install.before_install"
# after_install = "frappe_starter_theme.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "frappe_starter_theme.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"frappe_starter_theme.tasks.all"
# 	],
# 	"daily": [
# 		"frappe_starter_theme.tasks.daily"
# 	],
# 	"hourly": [
# 		"frappe_starter_theme.tasks.hourly"
# 	],
# 	"weekly": [
# 		"frappe_starter_theme.tasks.weekly"
# 	]
# 	"monthly": [
# 		"frappe_starter_theme.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "frappe_starter_theme.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "frappe_starter_theme.event.get_events"
# }

