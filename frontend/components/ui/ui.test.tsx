import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { describe, expect, it, vi } from "vitest";
import { Badge, StatusBadge, statusTone } from "./badge";
import { Button } from "./button";
import { ConfirmAction } from "./confirm-action";

describe("Phase 2 UI primitives", () => {
  it("renders semantic badge tones and loading/disabled button states", () => {
    render(<><StatusBadge status="ready" /><Badge tone="danger">Attention</Badge><Button loading>Save</Button><Button disabled>Disabled</Button></>);
    expect(screen.getByText("ready")).toHaveClass("ui-badge-success");
    expect(screen.getByText("Attention")).toHaveClass("ui-badge-danger");
    expect(screen.getByRole("button", { name: /Save/ })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Disabled" })).toBeDisabled();
    expect(statusTone("pending_dns")).toBe("warning");
  });

  it("requires an explicit confirmation and returns focus to the trigger", async () => {
    const onConfirm = vi.fn();
    render(<ConfirmAction label="Suspend site" title="Suspend this site?" description="This changes the site lifecycle." onConfirm={onConfirm} />);
    const trigger = screen.getByRole("button", { name: "Suspend site" });
    fireEvent.click(trigger);
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(onConfirm).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole("button", { name: "Cancel" }));
    await waitFor(() => expect(screen.queryByRole("dialog")).not.toBeInTheDocument());
    expect(document.activeElement).toBe(trigger);
    fireEvent.click(trigger);
    fireEvent.click(screen.getByRole("button", { name: "Confirm" }));
    await waitFor(() => expect(onConfirm).toHaveBeenCalledTimes(1));
  });
});
