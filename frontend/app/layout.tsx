import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "SaaS Control Plane",
    template: "%s | SaaS Control Plane",
  },
  description:
    "Launch-ready SaaS control plane for onboarding organizations, managing tenants, and preparing ERPNext-backed operations without collapsing the product and runtime boundaries.",
  applicationName: "SaaS Control Plane",
  openGraph: {
    title: "SaaS Control Plane",
    description:
      "Manage organizations, tenants, implementation readiness, and rollout coordination before live ERPNext cutover.",
    type: "website",
  },
  twitter: {
    card: "summary",
    title: "SaaS Control Plane",
    description:
      "Manage organizations, tenants, implementation readiness, and rollout coordination before live ERPNext cutover.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function () {
                try {
                  var theme = localStorage.getItem('crm-theme');
                  if (theme !== 'light' && theme !== 'dark') {
                    theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
                  }
                  document.documentElement.dataset.theme = theme;
                  document.documentElement.classList.toggle('dark', theme === 'dark');
                } catch (error) {}
              })();
            `,
          }}
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
