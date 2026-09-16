import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Bricolage_Grotesque } from "next/font/google";
import { env } from "@/lib/env";
import "./globals.css";

const bricolage = Bricolage_Grotesque({
  subsets: ["latin"],
  weight: ["600", "700", "800"],
  variable: "--font-heading",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: env.appName,
    template: `%s | ${env.appName}`,
  },
  description:
    "Operator workspace for onboarding customers, managing ERP sites, packaging modules, and coordinating delivery readiness.",
  applicationName: env.appName,
  openGraph: {
    title: env.appName,
    description: "Operator workspace for customer onboarding, ERP site visibility, and delivery readiness.",
    type: "website",
  },
  twitter: {
    card: "summary",
    title: env.appName,
    description: "Operator workspace for customer onboarding, ERP site visibility, and delivery readiness.",
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
