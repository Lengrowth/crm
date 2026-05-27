# Glossary

- **SaaS control layer** - the centralized application that manages customers, tenants, plans, billing state, modules, domains, and provisioning for the product.
- **ERPNext tenant site** - a separate ERPNext/Frappe instance later provisioned for each customer or environment.
- **Organization** - the customer company in the SaaS layer.
- **Tenant** - a managed ERPNext/Frappe environment linked to an organization.
- **Plan** - a commercial package that defines entitlements and pricing.
- **Module** - a capability or product area such as CRM, drilling, fleet, or reporting.
- **Subscription** - the billing relationship between an organization and a plan.
- **Provisioning job** - a durable record of a tenant setup workflow.
- **Domain mapping** - the association between a tenant and its system subdomain or custom domain.
- **Implementation project** - the onboarding and setup work needed to bring a tenant online.
- **ERPNext provisioning service** - the abstraction that will eventually create and configure ERPNext sites.
