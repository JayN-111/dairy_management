app_name = "dairy_management"
app_title = "Dairy Management"
app_publisher = "jaynasit111@gmail.com"
app_description = "Dairy Management System"
app_email = "jaynasit111@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "dairy_management",
# 		"logo": "/assets/dairy_management/logo.png",
# 		"title": "Dairy Management",
# 		"route": "/dairy_management",
# 		"has_permission": "dairy_management.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/dairy_management/css/dairy_management.css"
# app_include_js = "/assets/dairy_management/js/dairy_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/dairy_management/css/dairy_management.css"
# web_include_js = "/assets/dairy_management/js/dairy_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "dairy_management/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "dairy_management/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "dairy_management.utils.jinja_methods",
# 	"filters": "dairy_management.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "dairy_management.install.before_install"
# after_install = "dairy_management.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "dairy_management.uninstall.before_uninstall"
# after_uninstall = "dairy_management.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "dairy_management.utils.before_app_install"
# after_app_install = "dairy_management.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "dairy_management.utils.before_app_uninstall"
# after_app_uninstall = "dairy_management.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "dairy_management.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
    "Milk Test Sample": {
        "validate": "dairy_management.doctype.milk_test_sample.milk_test_sample.MilkTestSample.validate",
        "on_submit": "dairy_management.doctype.milk_test_sample.milk_test_sample.MilkTestSample.on_submit",
        "on_update_after_submit": "dairy_management.doctype.milk_test_sample.milk_test_sample.MilkTestSample.on_update_after_submit",
        "after_workflow_action": "dairy_management.doctype.milk_test_sample.milk_test_sample.MilkTestSample.after_workflow_action",
        "notify_approvers": "dairy_management.doctype.milk_test_sample.milk_test_sample.MilkTestSample.notify_approvers",
        "notify_submitter": "dairy_management.doctype.milk_test_sample.milk_test_sample.MilkTestSample.notify_submitter",
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"dairy_management.tasks.all"
# 	],
# 	"daily": [
# 		"dairy_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"dairy_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"dairy_management.tasks.weekly"
# 	],
# 	"monthly": [
# 		"dairy_management.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "dairy_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "dairy_management.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "dairy_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["dairy_management.utils.before_request"]
# after_request = ["dairy_management.utils.after_request"]

# Job Events
# ----------
# before_job = ["dairy_management.utils.before_job"]
# after_job = ["dairy_management.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"dairy_management.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

