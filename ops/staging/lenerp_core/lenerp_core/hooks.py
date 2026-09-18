app_name = "lenerp_core"
app_title = "LenERP Core"
app_publisher = "LenERP"
app_description = "LenERP custom Frappe application boundary"
app_email = ""
app_license = "MIT"

# Keep site-specific values out of the app. The install hook only creates
# reusable roles and workflow metadata; demo values are opt-in through the
# explicit `bench execute lenerp_core.demo_seed.seed` command.
after_install = "lenerp_core.install.after_install"
after_migrate = "lenerp_core.install.after_migrate"
