"use client";

import * as DialogPrimitive from "@radix-ui/react-dialog";
import { X } from "lucide-react";
import type { ComponentPropsWithoutRef, ElementRef } from "react";
import { forwardRef } from "react";
import { cn } from "./utils";

export const Dialog = DialogPrimitive.Root;
export const DialogTrigger = DialogPrimitive.Trigger;
export const DialogClose = DialogPrimitive.Close;
export const DialogPortal = DialogPrimitive.Portal;

export const DialogContent = forwardRef<ElementRef<typeof DialogPrimitive.Content>, ComponentPropsWithoutRef<typeof DialogPrimitive.Content>>(
  ({ className, children, ...props }, ref) => <DialogPortal><DialogPrimitive.Overlay className="ui-overlay" /><DialogPrimitive.Content ref={ref} className={cn("ui-dialog-content", className)} {...props}>{children}<DialogPrimitive.Close className="ui-dialog-close" aria-label="Close dialog"><X className="h-4 w-4" /></DialogPrimitive.Close></DialogPrimitive.Content></DialogPortal>,
);
DialogContent.displayName = DialogPrimitive.Content.displayName;
export const DialogTitle = forwardRef<ElementRef<typeof DialogPrimitive.Title>, ComponentPropsWithoutRef<typeof DialogPrimitive.Title>>(({ className, ...props }, ref) => <DialogPrimitive.Title ref={ref} className={cn("ui-dialog-title", className)} {...props} />);
DialogTitle.displayName = DialogPrimitive.Title.displayName;
export const DialogDescription = forwardRef<ElementRef<typeof DialogPrimitive.Description>, ComponentPropsWithoutRef<typeof DialogPrimitive.Description>>(({ className, ...props }, ref) => <DialogPrimitive.Description ref={ref} className={cn("ui-dialog-description", className)} {...props} />);
DialogDescription.displayName = DialogPrimitive.Description.displayName;
