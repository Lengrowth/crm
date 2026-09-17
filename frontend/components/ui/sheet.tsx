"use client";

import * as DialogPrimitive from "@radix-ui/react-dialog";
import { X } from "lucide-react";
import type { ComponentPropsWithoutRef, ElementRef } from "react";
import { forwardRef } from "react";
import { cn } from "./utils";

export const Sheet = DialogPrimitive.Root;
export const SheetTrigger = DialogPrimitive.Trigger;
export const SheetClose = DialogPrimitive.Close;
export const SheetContent = forwardRef<ElementRef<typeof DialogPrimitive.Content>, ComponentPropsWithoutRef<typeof DialogPrimitive.Content> & { side?: "left" | "right" }>(
  ({ className, children, side = "right", ...props }, ref) => <DialogPrimitive.Portal><DialogPrimitive.Overlay className="ui-overlay" /><DialogPrimitive.Content ref={ref} className={cn("ui-sheet-content", `ui-sheet-${side}`, className)} {...props}>{children}<DialogPrimitive.Close className="ui-dialog-close" aria-label="Close panel"><X className="h-4 w-4" /></DialogPrimitive.Close></DialogPrimitive.Content></DialogPrimitive.Portal>,
);
SheetContent.displayName = DialogPrimitive.Content.displayName;
export const SheetTitle = DialogPrimitive.Title;
export const SheetDescription = DialogPrimitive.Description;
