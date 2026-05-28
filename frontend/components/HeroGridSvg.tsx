import { useId } from "react";

export default function HeroGridSvg({ className }: { className?: string }) {
  const uid = useId().replace(/:/g, "");
  const patId = `grid-${uid}`;

  return (
    <svg
      className={`pointer-events-none absolute inset-0 h-full w-full ${className ?? ""}`}
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
      preserveAspectRatio="xMidYMid slice"
    >
      <defs>
        <pattern id={patId} width="56" height="56" patternUnits="userSpaceOnUse">
          <path
            d="M 56 0 L 0 0 0 56"
            fill="none"
            stroke="currentColor"
            strokeWidth="0.6"
          />
        </pattern>
      </defs>

      <rect
        width="100%"
        height="100%"
        fill={`url(#${patId})`}
        style={{ color: "var(--text)" }}
        opacity="0.15"
      />
    </svg>
  );
}
