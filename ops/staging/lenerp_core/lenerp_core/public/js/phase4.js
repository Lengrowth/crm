(function () {
  "use strict";

  function bootWorkspace() {
    var boot = window.frappe && window.frappe.boot;
    var rollout = boot && boot.lenerp_phase4_workspace;
    if (window.location.pathname === "/app" && rollout && rollout.enabled) {
      window.location.replace("/champion-home");
      return;
    }
    var root = document.getElementById("lenerp-phase4-root");
    if (!root || root.dataset.loaded === "true") return;
    root.dataset.loaded = "true";
    renderHome(root);
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value).replace(/[&<>'"]/g, function (character) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[character];
    });
  }

  function link(label, href, className) {
    return href ? '<a class="' + (className || "") + '" href="' + escapeHtml(href) + '">' + escapeHtml(label) + '</a>' : "";
  }

  function stateCard(message, className) {
    return '<div class="lenerp-phase4__state ' + (className || "") + '" role="status">' + escapeHtml(message) + '</div>';
  }

  function renderHome(root) {
    var api = root.dataset.api;
    var controller = new AbortController();
    var timeout = window.setTimeout(function () { controller.abort(); }, 8000);
    fetch(api, { credentials: "same-origin", headers: { Accept: "application/json" }, signal: controller.signal })
      .then(function (response) {
        if (response.status === 403) throw new Error("ACCESS_DENIED");
        if (!response.ok) throw new Error("FAILED");
        return response.json();
      })
      .then(function (payload) { renderPayload(root, payload.message || payload); })
      .catch(function (error) {
        var message = error && error.name === "AbortError" ? "This is taking longer than expected. Retry to load your work." : error.message === "ACCESS_DENIED" ? "Access denied. Your role is not authorized for this Champion workspace." : "The workspace could not load. Retry or open the standard ERP workspace.";
        root.querySelector(".lenerp-phase4__grid").innerHTML = stateCard(message, "lenerp-phase4__state--attention") + link("Retry", "/champion-home", "lenerp-phase4__action");
      })
      .finally(function () { window.clearTimeout(timeout); });
  }

  function renderPayload(root, data) {
    var nav = (data.navigation || []).map(function (item) { return link(item.label, item.route, ""); }).join("");
    var navById = (data.navigation || []).reduce(function (result, item) { result[item.id] = item; return result; }, {});
    var actions = (data.actions || []).map(function (action) {
      var destination = navById[action.nav];
      return destination ? link(action.label, destination.route, "lenerp-phase4__action") : '<div class="lenerp-phase4__action">' + escapeHtml(action.label) + '</div>';
    }).join("");
    var recent = (data.recent || []).map(function (record) {
      return '<div class="lenerp-phase4__record">' + link(record.subject || record.name || "Record", record.route) + '<small>' + escapeHtml(record.status || record.modified || "Authorized record") + '</small></div>';
    }).join("");
    var attention = (data.attention || []).map(function (item) { return '<div class="lenerp-phase4__record">' + link(item.label, item.route) + '<small>' + escapeHtml(item.description) + '</small></div>'; }).join("");
    var pending = (data.pending || []).map(function (item) { return '<div class="lenerp-phase4__record"><span>' + escapeHtml(item.source) + '</span><small>Pending configuration</small></div>'; }).join("");
    var recentBody = recent || stateCard("Nothing is assigned or recent yet. New work will appear here when an authorized ERP record exists.");
    var attentionBody = attention || stateCard("No attention items were found in the authorized records.");
    var pendingBody = pending || stateCard("All configured sources are available.");
    root.querySelector(".lenerp-phase4__grid").innerHTML = '<section class="lenerp-phase4__card"><h2>What you can do</h2><div class="lenerp-phase4__actions">' + actions + '</div></section>' + '<section class="lenerp-phase4__card"><h2>Recent or assigned work</h2>' + recentBody + '</section>' + '<section class="lenerp-phase4__card"><h2>Needs attention</h2>' + attentionBody + '</section>' + '<section class="lenerp-phase4__card"><h2>Champion navigation</h2><div class="lenerp-phase4__nav">' + nav + '</div></section>' + '<section class="lenerp-phase4__card"><h2>Configuration status</h2>' + pendingBody + '</section>' + '<section class="lenerp-phase4__card"><h2>Data source</h2>' + stateCard(data.state === "partial" ? "Some authorized sources are unavailable. The visible records are partial; retry later." : "This page uses authorized ERPNext/HRMS records. It does not create a second operational database.") + '</section>';
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", bootWorkspace, { once: true });
  else bootWorkspace();
})();
