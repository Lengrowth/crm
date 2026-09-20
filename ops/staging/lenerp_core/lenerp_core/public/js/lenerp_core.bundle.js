(function () {
  "use strict";

  function applicationName() {
    var bootName = window.frappe && window.frappe.boot && window.frappe.boot.sysdefaults
      ? window.frappe.boot.sysdefaults.app_name
      : "";
    return typeof bootName === "string" && bootName.trim() ? bootName.trim() : "LenERP";
  }

  function allowBrowserZoom() {
    var viewports = document.querySelectorAll('meta[name="viewport"]');
    if (!viewports.length) {
      var viewport = document.createElement("meta");
      viewport.name = "viewport";
      document.head.appendChild(viewport);
      viewports = [viewport];
    }

    viewports[0].setAttribute("content", "width=device-width, initial-scale=1");
    for (var index = 1; index < viewports.length; index += 1) {
      viewports[index].remove();
    }
  }

  function labelLogos() {
    var name = applicationName();
    var logos = document.querySelectorAll(
      "img.app-logo, .app-logo img, .navbar-brand img, img.footer-logo"
    );
    for (var index = 0; index < logos.length; index += 1) {
      logos[index].setAttribute("alt", name);
    }

    var splashImages = document.querySelectorAll(".splash img");
    for (var splashIndex = 0; splashIndex < splashImages.length; splashIndex += 1) {
      splashImages[splashIndex].setAttribute("alt", "");
    }
  }

  function labelUnlabelledSelects() {
    var selects = document.querySelectorAll("select");
    for (var index = 0; index < selects.length; index += 1) {
      var select = selects[index];
      if (select.getAttribute("aria-label") || select.labels && select.labels.length) continue;
      var source = select.getAttribute("data-fieldname") || select.getAttribute("name") || select.id || "Select option";
      var label = source.replaceAll("-", " ").replaceAll("_", " ").trim();
      select.setAttribute("aria-label", label || "Select option");
    }
  }

  function apply() {
    allowBrowserZoom();
    labelLogos();
    labelUnlabelledSelects();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", apply, { once: true });
  } else {
    apply();
  }

  if (window.MutationObserver) {
    new MutationObserver(function (mutations) {
      for (var index = 0; index < mutations.length; index += 1) {
        if (mutations[index].addedNodes.length) {
          apply();
          break;
        }
      }
    }).observe(document.documentElement, { childList: true, subtree: true });
  }
})();

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

  document.addEventListener("DOMContentLoaded", function () {
    if (window.location.pathname === "/login") addCentralLogin();
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
