import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Bricolage_Grotesque } from "next/font/google";
import "./globals.css";

const bricolage = Bricolage_Grotesque({
  subsets: ["latin"],
  weight: ["600", "700", "800"],
  variable: "--font-heading",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "LenERP Control Plane",
    template: "%s | LenERP Control Plane",
  },
  description:
    "Launch-ready SaaS control for onboarding organizations, managing tenants, packaging modules, and coordinating ERPNext-backed operational rollouts without collapsing the product and runtime boundaries.",
  applicationName: "LenERP Control Plane",
  openGraph: {
    title: "LenERP Control Plane",
    description:
      "Premium SaaS control for onboarding, implementation visibility, tenant readiness, and ERPNext-aware rollout coordination.",
    type: "website",
  },
  twitter: {
    card: "summary",
    title: "LenERP Control Plane",
    description:
      "Premium SaaS control for onboarding, implementation visibility, tenant readiness, and ERPNext-aware rollout coordination.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning className={bricolage.variable}>
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
