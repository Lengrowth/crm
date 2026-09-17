"use client";

import Link from "next/link";
import {
  AnimatePresence,
  motion,
  useMotionValue,
  useReducedMotion,
  useSpring,
  useTransform,
} from "framer-motion";
import { useEffect, useState, type CSSProperties, type PointerEvent, type ReactNode } from "react";
import { MarketingButtonLink, ScrollReveal } from "@/components/MarketingPrimitives";

const ease = [0.22, 1, 0.36, 1] as const;

type IconName =
  | "brand"
  | "tenant"
  | "revenue"
  | "modules"
  | "support"
  | "workflow"
  | "arrow"
  | "check"
  | "globe"
  | "shield"
  | "spark";

function Icon({ name, className = "h-5 w-5" }: { name: IconName; className?: string }) {
  const common = {
    className,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.7,
    strokeLinecap: "round" as const,
    strokeLinejoin: "round" as const,
    "aria-hidden": true,
  };

  const paths: Record<IconName, ReactNode> = {
    brand: <><path d="M5 19 19 5" /><path d="m14 5 5 5" /><path d="M5 14v5h5" /><path d="M7.5 11.5 12.5 6.5" /></>,
    tenant: <><rect x="3.5" y="4" width="17" height="16" rx="2" /><path d="M7.5 8h3M13.5 8h3M7.5 12h3M13.5 12h3M9 20v-4h6v4" /></>,
    revenue: <><path d="M4 18.5h16" /><path d="m6 15 4-4 3 2 5-6" /><path d="M15 7h3v3" /></>,
    modules: <><rect x="4" y="4" width="6" height="6" rx="1.5" /><rect x="14" y="4" width="6" height="6" rx="1.5" /><rect x="4" y="14" width="6" height="6" rx="1.5" /><rect x="14" y="14" width="6" height="6" rx="1.5" /></>,
    support: <><circle cx="12" cy="12" r="8.5" /><path d="M8.7 14.5c.8 1 1.9 1.5 3.3 1.5s2.5-.5 3.3-1.5M9 9.5h.01M15 9.5h.01" /></>,
    workflow: <><circle cx="6" cy="6" r="2" /><circle cx="18" cy="18" r="2" /><path d="M8 6h5a3 3 0 0 1 3 3v7M16 12l-3-3 3-3" /></>,
    arrow: <><path d="M5 12h14" /><path d="m14 7 5 5-5 5" /></>,
    check: <path d="m5 12.5 4.2 4.2L19 7" />,
    globe: <><circle cx="12" cy="12" r="9" /><path d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18" /></>,
    shield: <><path d="M12 3 19 6v5.2c0 4.5-2.9 7.3-7 9-4.1-1.7-7-4.5-7-9V6l7-3Z" /><path d="m9 12 2 2 4-4" /></>,
    spark: <><path d="m12 3 1.7 5.3L19 10l-5.3 1.7L12 17l-1.7-5.3L5 10l5.3-1.7L12 3Z" /><path d="m18.5 16 .7 2.3 2.3.7-2.3.7-.7 2.3-.7-2.3-2.3-.7 2.3-.7.7-2.3Z" /></>,
  };

  return <svg {...common}>{paths[name]}</svg>;
}

function SectionLabel({ index, children }: { index: string; children: ReactNode }) {
  return (
    <div className="reseller-section-label">
      <span>{index}</span>
      <span>{children}</span>
    </div>
  );
}

function HeroProduct() {
  const reducedMotion = useReducedMotion();
  const pointerX = useMotionValue(0);
  const pointerY = useMotionValue(0);
  const springX = useSpring(pointerX, { stiffness: 90, damping: 24 });
  const springY = useSpring(pointerY, { stiffness: 90, damping: 24 });
  const rotateY = useTransform(springX, [-1, 1], [-7, 7]);
  const rotateX = useTransform(springY, [-1, 1], [6, -6]);

  function handlePointerMove(event: PointerEvent<HTMLDivElement>) {
    if (reducedMotion) return;
    const bounds = event.currentTarget.getBoundingClientRect();
    pointerX.set(((event.clientX - bounds.left) / bounds.width) * 2 - 1);
    pointerY.set(((event.clientY - bounds.top) / bounds.height) * 2 - 1);
  }

  return (
    <div
      className="reseller-hero-product"
      onPointerMove={handlePointerMove}
      onPointerLeave={() => {
        pointerX.set(0);
        pointerY.set(0);
      }}
    >
      <div className="reseller-orbit reseller-orbit-one" />
      <div className="reseller-orbit reseller-orbit-two" />
      <motion.div
        className="reseller-product-stack"
        style={{ rotateX, rotateY, transformPerspective: 1200 }}
      >
        <div className="reseller-product-shadow" />
        <motion.div
          className="reseller-float-card reseller-float-card-domain"
          animate={reducedMotion ? undefined : { y: [0, -8, 0] }}
          transition={{ duration: 4.8, repeat: Infinity, ease: "easeInOut" }}
        >
          <span className="reseller-status-dot" />
          <span>cloud.northstar.io</span>
        </motion.div>
        <motion.div
          className="reseller-float-card reseller-float-card-growth"
          animate={reducedMotion ? undefined : { y: [0, 7, 0] }}
          transition={{ duration: 5.4, repeat: Infinity, ease: "easeInOut", delay: -1.2 }}
        >
          <span className="text-[10px] uppercase tracking-[.18em] text-zinc-500">MRR</span>
          <strong>+24.8%</strong>
          <span className="reseller-mini-chart"><i /><i /><i /><i /><i /></span>
        </motion.div>

        <div className="reseller-product-window">
          <div className="reseller-window-bar">
            <div className="flex gap-1.5"><i /><i /><i /></div>
            <span>Northstar / Control centre</span>
            <b>NS</b>
          </div>
          <div className="reseller-window-body">
            <aside>
              <div className="reseller-window-logo">N</div>
              {[0, 1, 2, 3, 4].map((item) => <span key={item} className={item === 0 ? "active" : ""} />)}
            </aside>
            <div className="reseller-window-main">
              <div className="flex items-start justify-between">
                <div><small>GOOD MORNING, ALEX</small><h3>Business overview</h3></div>
                <span className="reseller-window-action">+ New customer</span>
              </div>
              <div className="reseller-kpi-row">
                <div><small>ACTIVE SITES</small><strong>38</strong><em>+4 this month</em></div>
                <div><small>MONTHLY REVENUE</small><strong>$18.4k</strong><em>↗ 12.8%</em></div>
                <div><small>OPEN PROJECTS</small><strong>09</strong><em>3 launching</em></div>
              </div>
              <div className="reseller-chart-card">
                <div className="flex items-center justify-between"><small>PARTNER GROWTH</small><span>Last 12 months</span></div>
                <svg viewBox="0 0 520 125" preserveAspectRatio="none" aria-hidden="true">
                  <defs><linearGradient id="partner-chart-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#b8f500" stopOpacity=".35"/><stop offset="1" stopColor="#b8f500" stopOpacity="0"/></linearGradient></defs>
                  <path d="M0 106C55 105 64 84 108 88s62 10 96-14 61-15 94-27 58 9 91-16 73-18 131-27V125H0Z" fill="url(#partner-chart-fill)" />
                  <path d="M0 106C55 105 64 84 108 88s62 10 96-14 61-15 94-27 58 9 91-16 73-18 131-27" fill="none" stroke="#84b300" strokeWidth="3" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}

const transformations = [
  { label: "Identity", title: "Your name leads.", body: "Replace every customer-facing surface with your identity, colors, typography, and voice.", accent: "#6257ff", domain: "portal.northstar.io", mark: "N" },
  { label: "Domain", title: "Your domain builds trust.", body: "Give every customer a polished workspace on infrastructure that looks and feels entirely yours.", accent: "#ff6b35", domain: "erp.coppercloud.co", mark: "C" },
  { label: "Product", title: "Your product takes shape.", body: "Choose the modules, vertical workflows, and customer experience that fit your market.", accent: "#16a36a", domain: "work.oliveops.com", mark: "O" },
  { label: "Revenue", title: "Your pricing creates value.", body: "Package subscriptions, implementation, support, and expertise into recurring customer relationships.", accent: "#1d7afc", domain: "hub.bluepeak.io", mark: "B" },
];

function TransformationStudio() {
  const [active, setActive] = useState(0);
  const reducedMotion = useReducedMotion();

  useEffect(() => {
    if (reducedMotion) return;
    const timer = window.setInterval(() => setActive((value) => (value + 1) % transformations.length), 5000);
    return () => window.clearInterval(timer);
  }, [reducedMotion]);

  const item = transformations[active];

  return (
    <div className="reseller-studio">
      <div className="reseller-studio-copy">
        <SectionLabel index="02">Make it yours</SectionLabel>
        <AnimatePresence mode="wait">
          <motion.div key={item.label} initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} transition={{ duration: .45, ease }}>
            <p className="reseller-studio-kicker">{item.label}</p>
            <h2>{item.title}</h2>
            <p className="reseller-body-copy">{item.body}</p>
          </motion.div>
        </AnimatePresence>
        <div className="reseller-studio-tabs" role="tablist" aria-label="White-label capabilities">
          {transformations.map((step, index) => (
            <button key={step.label} type="button" role="tab" aria-selected={active === index} onClick={() => setActive(index)}>
              <span>0{index + 1}</span>{step.label}
            </button>
          ))}
        </div>
      </div>
      <div className="reseller-brand-preview" style={{ "--partner-accent": item.accent } as CSSProperties}>
        <div className="reseller-preview-browser">
          <div className="reseller-preview-top"><i /><i /><i /><span>{item.domain}</span></div>
          <div className="reseller-preview-shell">
            <aside><b>{item.mark}</b><span className="active" /><span /><span /><span /></aside>
            <div className="reseller-preview-main">
              <div className="reseller-preview-head"><div><small>PARTNER WORKSPACE</small><strong>{item.domain.split(".")[1]?.toUpperCase()}</strong></div><i>{item.mark}</i></div>
              <div className="reseller-preview-grid"><div className="wide"><small>Portfolio performance</small><svg viewBox="0 0 300 85" preserveAspectRatio="none"><path d="M0 72C31 71 42 58 67 60s36 4 57-18 37 3 60-10 47 6 67-17 31-4 49-10" /></svg></div><div><small>Customers</small><strong>48</strong></div><div><small>Renewal</small><strong>96%</strong></div></div>
            </div>
          </div>
        </div>
        <AnimatePresence mode="wait"><motion.div key={item.domain} className="reseller-preview-swatch" initial={{ opacity: 0, scale: .92, y: 8 }} animate={{ opacity: 1, scale: 1, y: 0 }} exit={{ opacity: 0, scale: .92 }} transition={{ duration: .35 }}><span style={{ background: item.accent }} /><small>Brand applied</small><strong>{item.accent}</strong></motion.div></AnimatePresence>
      </div>
    </div>
  );
}

const capabilities = [
  { icon: "tenant" as IconName, index: "01", title: "Tenant command", body: "Provision, configure, monitor, and support every customer environment from one calm control centre.", className: "reseller-bento-command" },
  { icon: "brand" as IconName, index: "02", title: "Brand studio", body: "Own every touchpoint, from domain and login screen to documents and customer emails.", className: "reseller-bento-brand" },
  { icon: "revenue" as IconName, index: "03", title: "Revenue visibility", body: "See subscription value and customer growth without losing sight of delivery work.", className: "reseller-bento-revenue" },
  { icon: "modules" as IconName, index: "04", title: "Composable product", body: "Switch modules and workflows on as each customer's operation evolves.", className: "reseller-bento-modules" },
  { icon: "workflow" as IconName, index: "05", title: "Guided launches", body: "Turn discovery, configuration, migration, training, and go-live into a repeatable playbook.", className: "reseller-bento-workflow" },
  { icon: "support" as IconName, index: "06", title: "A partner behind you", body: "Build customer relationships with product and implementation expertise available when you need it.", className: "reseller-bento-support" },
];

function CapabilityBento() {
  return (
    <section className="reseller-section">
      <ScrollReveal>
        <div className="reseller-section-heading">
          <div><SectionLabel index="03">Partner operating system</SectionLabel><h2>Everything behind the brand.</h2></div>
          <p className="reseller-body-copy">A complete operating layer for launching customers, shaping the product, and building durable recurring revenue.</p>
        </div>
      </ScrollReveal>
      <div className="reseller-bento">
        {capabilities.map((item, index) => (
          <ScrollReveal key={item.title} delay={index * .04} className={item.className}>
            <article className="reseller-bento-card">
              <div className="reseller-bento-top"><span>{item.index}</span><Icon name={item.icon} /></div>
              {item.icon === "tenant" && <div className="reseller-bento-visual tenant-visual"><span /><span /><span /><i /></div>}
              {item.icon === "brand" && <div className="reseller-bento-visual brand-visual"><i /><i /><i /><b>Aa</b></div>}
              {item.icon === "revenue" && <div className="reseller-bento-visual revenue-visual"><span>$24.8k</span><svg viewBox="0 0 200 55" preserveAspectRatio="none"><path d="M0 48c22 0 24-14 45-13s23 8 41-6 29 5 46-7 32 2 68-18" /></svg></div>}
              {item.icon === "modules" && <div className="reseller-bento-visual modules-visual">{["CRM", "FIN", "OPS", "MFG"].map((label) => <span key={label}>{label}</span>)}</div>}
              {item.icon === "workflow" && <div className="reseller-bento-visual workflow-visual"><span>Discover</span><i /><span>Configure</span><i /><span>Launch</span></div>}
              {item.icon === "support" && <div className="reseller-bento-visual support-visual"><span>N</span><span>L</span><i>Online together</i></div>}
              <div className="reseller-bento-copy"><h3>{item.title}</h3><p>{item.body}</p></div>
            </article>
          </ScrollReveal>
        ))}
      </div>
    </section>
  );
}

function formatMoney(value: number) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value);
}

function RevenueCalculator() {
  const [customers, setCustomers] = useState(35);
  const [subscription, setSubscription] = useState(420);
  const [services, setServices] = useState(2800);
  const monthly = customers * subscription;
  const annualRecurring = monthly * 12;
  const launchRevenue = customers * services;
  const firstYear = annualRecurring + launchRevenue;
  const marker = Math.min(100, Math.max(5, ((monthly - 2500) / 48000) * 100));

  return (
    <section className="reseller-revenue-section reseller-section">
      <div className="reseller-revenue-intro">
        <SectionLabel index="04">The opportunity</SectionLabel>
        <h2>Build value that compounds.</h2>
        <p className="reseller-body-copy">Explore a simple partner scenario. Keep control of your packaging, commercial model, and customer relationships.</p>
        <div className="reseller-assumption"><Icon name="spark" className="h-4 w-4" /><span>Illustrative model—not a revenue promise.</span></div>
      </div>
      <div className="reseller-calculator">
        <div className="reseller-controls">
          <RangeControl label="Active customers" value={customers} min={5} max={120} step={1} display={`${customers}`} onChange={setCustomers} />
          <RangeControl label="Monthly subscription / customer" value={subscription} min={150} max={900} step={10} display={formatMoney(subscription)} onChange={setSubscription} />
          <RangeControl label="Average launch services" value={services} min={0} max={8000} step={100} display={formatMoney(services)} onChange={setServices} />
        </div>
        <div className="reseller-output">
          <div className="reseller-output-label"><span>Illustrative monthly recurring revenue</span><i>Live model</i></div>
          <AnimatePresence mode="popLayout"><motion.strong key={monthly} initial={{ opacity: .35, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .25 }}>{formatMoney(monthly)}</motion.strong></AnimatePresence>
          <div className="reseller-output-track"><motion.span animate={{ width: `${marker}%` }} transition={{ duration: .45, ease }} /></div>
          <div className="reseller-output-grid"><div><small>Annual recurring</small><b>{formatMoney(annualRecurring)}</b></div><div><small>Launch services</small><b>{formatMoney(launchRevenue)}</b></div><div><small>Illustrative year one</small><b>{formatMoney(firstYear)}</b></div></div>
          <p>Calculated as active customers × subscription × 12, plus one launch project per customer.</p>
        </div>
      </div>
    </section>
  );
}

function RangeControl({ label, value, min, max, step, display, onChange }: { label: string; value: number; min: number; max: number; step: number; display: string; onChange: (value: number) => void }) {
  const progress = ((value - min) / (max - min)) * 100;
  return (
    <label className="reseller-range-control">
      <span><small>{label}</small><strong>{display}</strong></span>
      <input type="range" min={min} max={max} step={step} value={value} onChange={(event) => onChange(Number(event.target.value))} style={{ "--range-progress": `${progress}%` } as CSSProperties} />
      <i><span>{min}</span><span>{max}</span></i>
    </label>
  );
}

const industries = [
  { name: "Manufacturing", code: "MFG", stat: "96.2%", statLabel: "On-time production", color: "#f0642b", chart: [35, 52, 44, 68, 62, 83, 91] },
  { name: "Distribution", code: "DST", stat: "4.8×", statLabel: "Stock velocity", color: "#6257ff", chart: [28, 44, 57, 49, 72, 79, 94] },
  { name: "Field services", code: "FLD", stat: "92%", statLabel: "First-time completion", color: "#16a36a", chart: [42, 39, 55, 61, 58, 77, 86] },
  { name: "Drilling", code: "DRL", stat: "18", statLabel: "Active field jobs", color: "#1d7afc", chart: [22, 36, 48, 43, 66, 71, 89] },
];

function IndustryWorlds() {
  const [active, setActive] = useState(0);
  const [catalogModules, setCatalogModules] = useState<string[]>([]);
  useEffect(() => {
    void fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000"}/public/modules`).then((response) => response.ok ? response.json() : []).then((items: Array<{ name: string }>) => setCatalogModules(items.map((item) => item.name))).catch(() => undefined);
  }, []);
  const industry = industries[active];
  const industryModules = catalogModules.slice(active * 3, active * 3 + 3);
  const points = industry.chart.map((value, index) => `${index * (300 / (industry.chart.length - 1))},${100 - value}`).join(" ");

  return (
    <section className="reseller-industries reseller-section">
      <div className="reseller-section-heading">
        <div><SectionLabel index="05">One engine, many businesses</SectionLabel><h2>Go vertical. Then go deeper.</h2></div>
        <p className="reseller-body-copy">Turn one adaptable platform into a focused offer for the industries you understand best.</p>
      </div>
      <div className="reseller-industry-stage" style={{ "--industry": industry.color } as CSSProperties}>
        <div className="reseller-industry-tabs" role="tablist" aria-label="Industries">
          {industries.map((item, index) => <button key={item.name} type="button" role="tab" aria-selected={index === active} onClick={() => setActive(index)}><span>0{index + 1}</span>{item.name}</button>)}
        </div>
        <div className="reseller-industry-product">
          <AnimatePresence mode="wait">
            <motion.div key={industry.name} className="reseller-industry-window" initial={{ opacity: 0, y: 18, scale: .985 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: -10 }} transition={{ duration: .45, ease }}>
              <div className="reseller-industry-nav"><b>{industry.code}</b><div><span className="active" /><span /><span /><span /></div><i>AB</i></div>
              <div className="reseller-industry-main">
                <div className="reseller-industry-header"><div><small>OPERATIONS / {industry.code}</small><h3>{industry.name} command</h3></div><span>Live overview</span></div>
                <div className="reseller-industry-dashboard">
                  <div className="reseller-industry-chart"><small>Operational performance</small><svg viewBox="0 0 300 105" preserveAspectRatio="none"><polyline points={points} /></svg><div>{industryModules.map((module) => <span key={module}>{module}</span>)}</div></div>
                  <div className="reseller-industry-stat"><span className="reseller-live-dot" /><strong>{industry.stat}</strong><small>{industry.statLabel}</small><i>Live</i></div>
                </div>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>
      </div>
    </section>
  );
}

const journey = [
  { number: "01", title: "Shape the offer", body: "Choose your market, commercial model, brand, and the modules that make your offer distinctive.", icon: "brand" as IconName },
  { number: "02", title: "Configure the system", body: "Turn your expertise into repeatable workflows, roles, documents, dashboards, and implementation templates.", icon: "modules" as IconName },
  { number: "03", title: "Launch customers", body: "Move from signed agreement to an isolated, branded customer workspace through a guided delivery path.", icon: "tenant" as IconName },
  { number: "04", title: "Operate and grow", body: "Support customers, expand their modules, and see your recurring portfolio mature from one control centre.", icon: "revenue" as IconName },
];

function PartnerJourney() {
  const [active, setActive] = useState(0);
  return (
    <section className="reseller-journey reseller-section">
      <div className="reseller-journey-sticky">
        <SectionLabel index="06">The partner journey</SectionLabel>
        <h2>From expertise to product.</h2>
        <p className="reseller-body-copy">Your knowledge becomes more valuable when it is packaged in a system customers rely on every day.</p>
        <div className="reseller-journey-visual">
          <div className="reseller-journey-rings"><i /><i /><i /></div>
          <AnimatePresence mode="wait"><motion.div key={active} className="reseller-journey-core" initial={{ opacity: 0, scale: .75, rotate: -8 }} animate={{ opacity: 1, scale: 1, rotate: 0 }} exit={{ opacity: 0, scale: .75, rotate: 8 }} transition={{ duration: .4, ease }}><Icon name={journey[active].icon} className="h-8 w-8" /><span>{journey[active].number}</span></motion.div></AnimatePresence>
          {journey.map((item, index) => <span key={item.number} className={`reseller-journey-node node-${index + 1} ${active >= index ? "active" : ""}`}>{item.number}</span>)}
        </div>
      </div>
      <div className="reseller-journey-steps">
        {journey.map((item, index) => (
          <motion.article key={item.number} className={active === index ? "active" : ""} onViewportEnter={() => setActive(index)} viewport={{ amount: .62 }}>
            <div className="reseller-journey-step-top"><span>{item.number}</span><Icon name={item.icon} /></div>
            <h3>{item.title}</h3><p>{item.body}</p>
            <button type="button" onClick={() => setActive(index)}>Explore step <Icon name="arrow" className="h-4 w-4" /></button>
          </motion.article>
        ))}
      </div>
    </section>
  );
}

function Architecture() {
  return (
    <section className="reseller-architecture reseller-section">
      <div className="reseller-architecture-copy">
        <SectionLabel index="07">Built for trust</SectionLabel>
        <h2>One portfolio.<br />Clear boundaries.</h2>
        <p className="reseller-body-copy">Manage the relationship centrally while each customer operates in an isolated ERP site with its own domain, settings, users, and data.</p>
        <ul><li><Icon name="shield" />Isolated customer environments</li><li><Icon name="globe" />Custom domains and identity</li><li><Icon name="workflow" />Central provisioning and oversight</li></ul>
      </div>
      <div className="reseller-architecture-map">
        <svg className="reseller-architecture-lines" viewBox="0 0 700 460" preserveAspectRatio="none" aria-hidden="true"><path d="M350 96v68M350 164C350 220 136 194 136 278M350 164v114M350 164c0 56 214 30 214 114" /><path className="pulse" d="M350 96v68M350 164C350 220 136 194 136 278M350 164v114M350 164c0 56 214 30 214 114" /></svg>
        <div className="reseller-architecture-partner"><span>YOU</span><strong>Partner control</strong><small>Brand · Provision · Support</small></div>
        {[
          ["AL", "Atlas Manufacturing", "32 users"],
          ["NO", "Northline Services", "18 users"],
          ["VE", "Verde Distribution", "47 users"],
        ].map((customer, index) => <div key={customer[1]} className={`reseller-architecture-customer customer-${index + 1}`}><span>{customer[0]}</span><strong>{customer[1]}</strong><small><i />Isolated site · {customer[2]}</small></div>)}
        <div className="reseller-architecture-legend"><span><i />Encrypted connection</span><span><Icon name="shield" className="h-3.5 w-3.5" />Independent data boundary</span></div>
      </div>
    </section>
  );
}

export function ResellerExperience() {
  return (
    <div className="reseller-page">
      <section className="reseller-hero">
        <div className="reseller-hero-grid" aria-hidden="true" />
        <div className="reseller-hero-topline"><span>LenERP partner network</span><span>White-label business platform / 2026</span></div>
        <div className="reseller-hero-layout">
          <div className="reseller-hero-copy">
            <motion.div className="reseller-pill" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .5, ease }}><span /><span>Partner applications open</span><Icon name="arrow" className="h-3.5 w-3.5" /></motion.div>
            <h1 aria-label="Your brand. Our engine."><motion.span initial={{ opacity: 0, y: 45 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .75, delay: .05, ease }}>Your brand.</motion.span><motion.span className="reseller-outline-type" initial={{ opacity: 0, y: 45 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .75, delay: .12, ease }}>Our engine.</motion.span></h1>
            <motion.p initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .65, delay: .2, ease }}>Launch a complete ERP business under your own identity—without spending years building the platform beneath it.</motion.p>
            <motion.div className="reseller-hero-actions" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .65, delay: .28, ease }}><MarketingButtonLink href="/contact">Become a partner <Icon name="arrow" className="h-4 w-4" /></MarketingButtonLink><Link href="#how-it-works" className="reseller-text-link">See how it works <span>↓</span></Link></motion.div>
            <motion.div className="reseller-hero-proof" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: .8, delay: .4 }}><span><Icon name="check" />Your domain</span><span><Icon name="check" />Your pricing</span><span><Icon name="check" />Your customer</span></motion.div>
          </div>
          <motion.div initial={{ opacity: 0, scale: .96, x: 20 }} animate={{ opacity: 1, scale: 1, x: 0 }} transition={{ duration: .9, delay: .15, ease }}><HeroProduct /></motion.div>
        </div>
        <div className="reseller-hero-marquee"><div>{["Brand it", "Package it", "Launch it", "Grow it", "Own the relationship", "Brand it", "Package it", "Launch it"].map((item, index) => <span key={`${item}-${index}`}>{item}<i /></span>)}</div></div>
      </section>

      <section id="how-it-works" className="reseller-transformation reseller-section"><TransformationStudio /></section>
      <CapabilityBento />
      <RevenueCalculator />
      <IndustryWorlds />
      <PartnerJourney />
      <Architecture />

      <section className="reseller-final-cta">
        <div className="reseller-final-grid" aria-hidden="true" />
        <div className="reseller-final-badge"><span>08</span><span>Your next chapter</span></div>
        <h2>The next ERP company<br />could be <em>yours.</em></h2>
        <p>Bring the market knowledge. We’ll bring the platform, infrastructure, and implementation foundation.</p>
        <div className="reseller-final-actions"><MarketingButtonLink href="/contact">Apply to become a partner <Icon name="arrow" className="h-4 w-4" /></MarketingButtonLink><MarketingButtonLink href="/demo" variant="secondary">Book a platform tour</MarketingButtonLink></div>
        <div className="reseller-final-foot"><span>LenERP partner network</span><span>Built for operators, implementers, and industry experts.</span></div>
      </section>
    </div>
  );
}
