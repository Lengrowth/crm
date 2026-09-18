from __future__ import annotations

import json

from app.integrations.frappe_bench import FrappeBenchERPNextClient


def _client(tmp_path):
    return FrappeBenchERPNextClient(bench_root=str(tmp_path), site_prefix="phase4-")


def test_list_apps_reads_frappe_json_output(tmp_path, monkeypatch):
    client = _client(tmp_path)
    output = json.dumps({"phase4-example.test": ["frappe", "erpnext", "lenerp_core"]})
    monkeypatch.setattr(client, "_run", lambda args: (True, output))

    assert client._list_apps("phase4-example.test") == {
        "frappe": "",
        "erpnext": "",
        "lenerp_core": "",
    }


def test_show_config_reads_frappe_json_output(tmp_path, monkeypatch):
    client = _client(tmp_path)
    config = {"db_name": "phase4_example", "lenerp_phase4_modules": ["module_a"]}
    monkeypatch.setattr(
        client,
        "_run",
        lambda args: (True, json.dumps({"phase4-example.test": config})),
    )

    assert client._show_config("phase4-example.test") == config
