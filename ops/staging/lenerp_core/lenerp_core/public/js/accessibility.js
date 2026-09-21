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

    // The loading mark is decorative because it communicates no information
    // that is not already conveyed by the surrounding application shell.
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

  // Frappe replaces the desk body and navbar during route changes. Reapply
  // only when mutations add a new logo or viewport declaration.
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
