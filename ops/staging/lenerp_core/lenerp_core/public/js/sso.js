(function () {
  "use strict";

  function begin(nextPath) {
    var path = nextPath || window.location.pathname + window.location.search;
    return fetch("/api/method/lenerp_core.sso.begin?next_path=" + encodeURIComponent(path), {
      credentials: "same-origin",
      headers: { Accept: "application/json" },
    }).then(function (response) {
      if (!response.ok) throw new Error("Central sign-in is unavailable.");
      return response.json();
    }).then(function (payload) {
      var url = payload.message && payload.message.authorization_url;
      if (!url) throw new Error("Central sign-in did not return a safe destination.");
      window.location.assign(url);
    });
  }

  function addCentralLogin() {
    if (window.frappe && frappe.session && frappe.session.user !== "Guest") return;
    if (document.querySelector("[data-lenerp-central-login]")) return;
    var container = document.querySelector(".for-login, .login-content, form");
    if (!container) return;
    var link = document.createElement("a");
    link.href = "/api/method/lenerp_core.sso.begin?next_path=%2Fapp";
    link.dataset.lenerpCentralLogin = "true";
    link.className = "btn btn-primary btn-block";
    link.textContent = "Sign in with LenERP Control Plane";
    link.setAttribute("aria-label", "Sign in with LenERP Control Plane");
    link.style.marginTop = "0.75rem";
    container.appendChild(link);
  }

  function addControlPlaneLink() {
    var url = window.frappe && frappe.boot && frappe.boot.lenerp_control_plane_return_url;
    if (!url || document.querySelector("[data-lenerp-control-plane]") || !document.body) return;
    var link = document.createElement("a");
    link.href = url;
    link.target = "_self";
    link.rel = "noopener";
    link.dataset.lenerpControlPlane = "true";
    link.className = "dropdown-item";
    link.textContent = (frappe.boot.lenerp_control_plane_label || "LenERP Control Plane");
    link.setAttribute("aria-label", "Return to LenERP Control Plane");
    var menus = document.querySelectorAll(".dropdown-menu");
    if (menus.length) menus[menus.length - 1].appendChild(link);
  }

  function directAppVisit() {
    if (!window.frappe || !frappe.session || frappe.session.user !== "Guest") return;
    if (window.location.pathname === "/app") {
      begin("/app").catch(function () { /* the login surface remains available for break-glass support */ });
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (window.location.pathname === "/login") addCentralLogin();
    directAppVisit();
    addControlPlaneLink();
    var observer = new MutationObserver(addControlPlaneLink);
    observer.observe(document.body, { childList: true, subtree: true });
    var attempts = 0;
    var retry = window.setInterval(function () {
      addControlPlaneLink();
      attempts += 1;
      if (document.querySelector("[data-lenerp-control-plane]") || attempts >= 40) {
        window.clearInterval(retry);
      }
    }, 250);
  });
})();
