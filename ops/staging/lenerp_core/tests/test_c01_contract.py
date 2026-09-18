import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
DOCTYPE = ROOT / "lenerp_core" / "len_erp_core" / "doctype" / "lenerp_branding_settings" / "lenerp_branding_settings.json"


def test_c01_doctype_is_value_free_and_system_manager_only():
	data = json.loads(DOCTYPE.read_text(encoding="utf-8"))

	assert data["name"] == "LenERP Branding Settings"
	assert data["issingle"] == 1
	assert [permission["role"] for permission in data["permissions"]] == ["System Manager"]
	assert not any(field.get("default") for field in data["fields"])

	field_names = {field["fieldname"] for field in data["fields"]}
	assert {
		"legal_name",
		"operating_name",
		"timezone",
		"currency",
		"fiscal_year_start",
		"product_name",
		"brand_mode",
		"logo",
		"favicon",
		"final_domain",
	}.issubset(field_names)

	serialized = DOCTYPE.read_text(encoding="utf-8")
	assert "lengrowth.com" not in serialized
