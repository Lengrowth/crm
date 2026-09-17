import type { TableHTMLAttributes, TdHTMLAttributes, ThHTMLAttributes } from "react";
import { cn } from "./utils";

export function Table({ className, ...props }: TableHTMLAttributes<HTMLTableElement>) { return <div className="ui-table-wrap"><table className={cn("ui-table", className)} {...props} /></div>; }
export function TableHeader({ className, ...props }: TableHTMLAttributes<HTMLTableSectionElement>) { return <thead className={cn("ui-table-header", className)} {...props} />; }
export function TableBody({ className, ...props }: TableHTMLAttributes<HTMLTableSectionElement>) { return <tbody className={cn("ui-table-body", className)} {...props} />; }
export function TableRow({ className, ...props }: TableHTMLAttributes<HTMLTableRowElement>) { return <tr className={cn("ui-table-row", className)} {...props} />; }
export function TableHead({ className, ...props }: ThHTMLAttributes<HTMLTableCellElement>) { return <th className={cn("ui-table-head", className)} {...props} />; }
export function TableCell({ className, ...props }: TdHTMLAttributes<HTMLTableCellElement>) { return <td className={cn("ui-table-cell", className)} {...props} />; }
