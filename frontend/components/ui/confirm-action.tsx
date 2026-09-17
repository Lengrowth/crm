"use client";

import { useState } from "react";
import { Button, type ButtonVariant } from "./button";
import { Dialog, DialogContent, DialogDescription, DialogTitle, DialogTrigger } from "./dialog";

export function ConfirmAction({ label, title, description, confirmLabel = "Confirm", variant = "danger", onConfirm, disabled }: { label: string; title: string; description: string; confirmLabel?: string; variant?: ButtonVariant; onConfirm: () => Promise<void> | void; disabled?: boolean }) {
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  async function confirm() { setBusy(true); try { await onConfirm(); setOpen(false); } finally { setBusy(false); } }
  return <Dialog open={open} onOpenChange={setOpen}><DialogTrigger asChild><Button type="button" variant={variant} disabled={disabled}>{label}</Button></DialogTrigger><DialogContent><DialogTitle>{title}</DialogTitle><DialogDescription>{description}</DialogDescription><div className="mt-6 flex justify-end gap-3"><Button type="button" variant="ghost" onClick={() => setOpen(false)}>Cancel</Button><Button type="button" variant={variant} loading={busy} onClick={confirm}>{confirmLabel}</Button></div></DialogContent></Dialog>;
}
