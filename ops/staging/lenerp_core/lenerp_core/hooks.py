app_name = "lenerp_core"
app_title = "LenERP Core"
app_publisher = "LenERP"
app_description = "LenERP custom Frappe application boundary"
app_email = ""
app_license = "MIT"

# Apply the accessibility boundary to both authenticated desk pages and public
# Frappe pages (including login, password recovery, and the loading shell).
# These are app-owned assets; the pinned Frappe/ERPNext sources remain
# unchanged.
app_include_js = [
    "/assets/lenerp_core/js/accessibility.js",
    "/assets/lenerp_core/js/sso.js",
]
web_include_js = [
    "/assets/lenerp_core/js/accessibility.js",
    "/assets/lenerp_core/js/sso.js",
]
update_website_context = ["lenerp_core.accessibility.update_context"]
base_template = "lenerp_core/templates/base.html"

# Keep site-specific values out of the app. The install hook only creates
# reusable roles and workflow metadata; demo values are opt-in through the
# explicit `bench execute lenerp_core.demo_seed.seed` command.
after_install = "lenerp_core.install.after_install"
before_migrate = "lenerp_core.install.before_migrate"
after_migrate = "lenerp_core.install.after_migrate"
extend_bootinfo = "lenerp_core.sso.extend_bootinfo"
on_login = "lenerp_core.sso.on_login"
