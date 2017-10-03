from __future__ import unicode_literals
import frappe

from frappe import _
from frappe.website.utils import find_first_image, get_comment_list
from frappe.utils import today, cint, global_date_format, get_fullname, strip_html_tags, markdown
from frappe.website.doctype.website_theme.website_theme import get_active_theme
from dti_devtools.debug import pretty_json

def get_starter_theme_context(context):
	if not hasattr(frappe.local, "request"):
		return
	
	path_name = frappe.local.request.path
	page = None

	if path_name == "/":
		path_name = frappe.db.get_single_value("Website Settings", "home_page")

	find_page = frappe.db.get_all("Web Page", filters={"route": path_name}, limit=1)

	if find_page:
		page = frappe.get_doc("Web Page", find_page[0].name)

	theme = get_active_theme()
	page_theme = None
	if page and page.theme_override:
		page_theme = frappe.get_doc("Website Theme", page.theme_override)
		if page.theme_override_mode == "Full":
			theme = page_theme
			page_theme = None

	if not frappe.local.conf.get("website_context"):
		frappe.local.conf["website_context"] = {}

	theme_values = {}
	for fieldname in theme.as_dict().keys():
		if fieldname.startswith("theme_"):
			theme_values[fieldname] = theme.get(fieldname)
			if page_theme and page_theme.get(fieldname):
				theme_values[fieldname] = page_theme.get(fieldname)

	if theme_values.get("theme_display_blog") != "No Display":
		get_blog_context(theme_values)

	frappe.local.conf['website_context'].update(theme_values)

def get_blog_context(context):

	context["blog_fields"] = ["published_on", "blog_intro", "route", "title", "content", "name", "blog_category"]
	context["blog_conditions"] = ""

	hooks = frappe.get_hooks("starter_theme_blog_context_before")
	for hook in hooks:
		frappe.call(hook, context)

	#posts = frappe.get_all("Blog Post", fields=context["blog_fields"], filters={"published": 1}, order_by="published_on desc, creation desc", limit=cint(context.get("theme_display_blog_length", 4)))

	query = """\
		select
			%(fields)s,
			ifnull(t1.blog_intro, t1.content) as intro,
			t2.full_name, t2.avatar, t1.blogger,
			(select count(name) from `tabCommunication`
			where
				communication_type='Comment'
				and comment_type='Comment'
				and reference_doctype='Blog Post'
				and reference_name=t1.name) as comments
		from `tabBlog Post` t1, `tabBlogger` t2
		where ifnull(t1.published,0)=1
			and t1.blogger = t2.name
			%(condition)s
		order by published_on desc, t1.creation desc
		limit %(start)s, %(page_len)s""" % {
			"start": 0, "page_len": cint(context.get("theme_display_blog_length", 4)),
			"condition": (" and " + " and ".join(context["blog_conditions"])) if context.get("blog_conditions") else "",
			"fields": ",".join(["t1.%s" % field for field in context["blog_fields"]])
		}

	posts = frappe.db.sql(query, as_dict=1)

	for post in posts:
		post.cover_image = find_first_image(post.content)
		post.published = global_date_format(post.creation)
		post.content = strip_html_tags(post.content[:340])
		post.intro = post.blog_intro if post.blog_intro else post.content
		if not post.comments:
			post.comment_text = _('No comments yet')
		elif post.comments==1:
			post.comment_text = _('1 comment')
		else:
			post.comment_text = _('{0} comments').format(str(post.comments))

		post.avatar = post.avatar or ""
		post.category = frappe.db.get_value('Blog Category', post.blog_category,
			['route', 'title'], as_dict=True)

		if (not "http:" in post.avatar or "https:" in post.avatar) and not post.avatar.startswith("/"):
			post.avatar = "/" + post.avatar

	context["blog_posts"] = posts

	hooks = frappe.get_hooks("starter_theme_blog_context_after")
	for hook in hooks:
		frappe.call(hook, context)
