# Surface — Finanzas (Pháros · Timón)

**Audience:** administrative & financial team
**App / surface:** `Pháros · Timón` (the ERP / finance suite — tenant: LCH `finance-lch`)
**Priorities:** numeric precision, data density, tables, KPIs, export.

> Built on the registry token contract — [`../tokens.css`](../tokens.css). This file
> carries the *durable intent*; the contract carries the *values*. Reference only
> semantic tokens (shadcn vars + the accent-independent status palette); never raw
> hex, never the old `--fin-*` / `--color-navy` / `--color-brand-red` mechanics.

---

## Accent

Finanzas is the **ERP · Timón** sub-brand, whose accent is **LCH Navy `#003A70`**
(+ teal `#A0D1CA` as the dark-mode accent / success) — **LOCKED** (RFC 0008 Q6).
That accent already lives in `--primary` / `--accent` / `--ring` / `--sidebar-primary`
in `tokens.css`, so this surface needs **no per-app override** — it consumes the
contract defaults as-is. Use `bg-primary` / `text-primary` / `ring-ring`; never
hard-code the navy.

---

## Status palette (accent-independent)

Money carries meaning through the **shared status palette**, which never shifts when
a sub-brand re-accents. Map the finance semantics onto it exactly:

| Finance meaning | Token | Utility |
|---|---|---|
| positive / income / paid | `--success` (teal) | `text-success` · `bg-success/20` |
| pending / due-soon / drift | `--warning` (yellow) | `bg-warning/40` · `text-warning-foreground` |
| overdue / negative / critical | `--error` / `--destructive` (red) | `text-error` · `bg-error/10` |
| informational / resolved / voided-note | `--info` (blue) | `text-info` · `bg-info/10` |

Red is reserved for **error/overdue** (and the family pilot light) — never use it as
a primary action colour. Primary actions use `--primary`.

---

## Typography & numerics

**Fundamental rule:** every monetary value and figure uses `font-mono`
(**IBM Plex Mono**) with `tabular-nums`. No exceptions. (JetBrains Mono is gone;
display type is Fraunces, UI sans is Inter.)

| Role | Tailwind |
|---|---|
| KPI amount (large) | `font-mono text-3xl font-semibold tabular-nums tracking-tight` |
| Table money cell | `font-mono text-sm tabular-nums` |
| Column header | `font-mono text-xs uppercase tracking-wide font-medium` |
| Label / caption | `font-mono text-xs text-muted-foreground` |

All theming is **`.dark`-aware** — because every colour above is a semantic token,
light/dark is handled by the contract; author once.

### Value formatting (unchanged domain logic)

```ts
// Currency: always Intl.NumberFormat
const formatCurrency = (amount: number, currency = 'COP') =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency }).format(amount)

// Dates: DD/MM/YYYY for display
const formatDate = (iso: string) =>
  new Date(iso).toLocaleDateString('es-CO', { day: '2-digit', month: '2-digit', year: 'numeric' })
```

---

## Component inventory

Names re-expressed on the Pháros contract (drop the `Lch` / `LchFinanzas` prefix —
a tenant never prefixes an app surface). These are the design-intent contracts; the
shadcn-vue SFCs are the Phase-1 build (RFC 0008).

### `KpiCard` — primary financial indicator
Props: `label: string`, `amount: number`, `currency?: string`, `trend?: 'up' | 'down' | 'flat'`, `delta?: number`, `periodo?: string`

```vue
<KpiCard label="Ingresos del mes" :amount="48500000" currency="COP"
         trend="up" :delta="12.5" periodo="Abril 2026" />
```

```vue
<!-- internal pattern -->
<div class="bg-card text-card-foreground border border-border rounded-lg p-5 shadow-sm">
  <p class="font-mono text-xs text-muted-foreground uppercase tracking-wide">{{ label }}</p>
  <p class="font-mono text-3xl font-semibold text-foreground tabular-nums mt-2 tracking-tight">
    {{ formatCurrency(amount) }}
  </p>
  <div class="flex items-center gap-1 mt-2">
    <Icon :name="trend === 'up' ? 'arrow-up' : 'arrow-down'" class="w-4 h-4"
          :class="trend === 'up' ? 'text-success' : 'text-error'" />
    <span class="font-mono text-sm"
          :class="trend === 'up' ? 'text-success' : 'text-error'">{{ delta }}%</span>
  </div>
</div>
```

### `DataTable` — financial table
Props: `columns: TableColumn[]`, `data: Record<string, any>[]`, `totals?: Record<string, number>`, `loading?: boolean`

```ts
interface TableColumn {
  key: string
  label: string
  type: 'text' | 'currency' | 'date' | 'status' | 'badge'
  align?: 'left' | 'right' | 'center'
}
```

```vue
<DataTable
  :columns="[
    { key: 'fecha',    label: 'Fecha',    type: 'date' },
    { key: 'concepto', label: 'Concepto', type: 'text' },
    { key: 'monto',    label: 'Monto',    type: 'currency', align: 'right' },
    { key: 'estado',   label: 'Estado',   type: 'badge' }
  ]"
  :data="facturas" :totals="{ monto: totalMes }" />
```

### `EstadoBadge` — transaction state
Props: `estado: 'pagado' | 'pendiente' | 'vencido' | 'anulado'`

```vue
<!-- pagado    → success -->
<span class="bg-success/20 text-success-foreground px-3 py-1 rounded-full text-xs font-medium">Pagado</span>
<!-- pendiente → warning -->
<span class="bg-warning/40 text-warning-foreground px-3 py-1 rounded-full text-xs font-medium">Pendiente</span>
<!-- vencido   → error -->
<span class="bg-error/10 text-error px-3 py-1 rounded-full text-xs font-medium">Vencido</span>
<!-- anulado   → muted/info -->
<span class="bg-muted text-muted-foreground px-3 py-1 rounded-full text-xs font-medium">Anulado</span>
```

### `CurrencyInput` — amount input
Props: `currency?: string`, `min?: number`, `max?: number`, `label?: string`

```vue
<CurrencyInput currency="COP" :min="0" label="Monto de factura" />
```

### `ExportBtn` — export action
Props: `format: 'pdf' | 'excel' | 'csv'`, `loading?: boolean`

---

## Domain patterns

### Financial table header
```vue
<thead class="bg-primary text-primary-foreground">
  <tr>
    <th class="px-4 py-3 text-left font-mono text-xs uppercase tracking-wide">Concepto</th>
    <th class="px-4 py-3 text-right font-mono text-xs uppercase tracking-wide">Monto (COP)</th>
  </tr>
</thead>
```

### Positive / negative money cell
```vue
<td class="px-4 py-3 text-right font-mono text-sm tabular-nums"
    :class="amount >= 0 ? 'text-success' : 'text-error'">
  {{ formatCurrency(amount) }}
</td>
```

### Totals row
```vue
<tfoot class="border-t-2 border-primary bg-accent">
  <tr>
    <td class="px-4 py-3 font-semibold text-foreground">Total</td>
    <td class="px-4 py-3 text-right font-mono font-semibold text-foreground tabular-nums">
      {{ formatCurrency(total) }}
    </td>
  </tr>
</tfoot>
```

---

## Target paths (in a consuming app)
```
components/finanzas/KpiCard.vue
components/finanzas/DataTable.vue
components/finanzas/EstadoBadge.vue
components/finanzas/CurrencyInput.vue
components/finanzas/ExportBtn.vue
pages/finanzas/dashboard.vue
pages/finanzas/facturas.vue
pages/finanzas/reportes.vue
```

---

## Ported from `ds-lch-finanzas`; what changed

- **Tokens.** Removed the whole `--fin-*` block plus `var(--color-navy)`,
  `var(--color-brand-red)`, `--color-blue/-yellow/-gray-*` and every raw hex
  (`text-[#00843D]`, `bg-lch-*`). Re-expressed on shadcn semantic tokens + the
  accent-independent status palette: positive/income → `--success`,
  pending → `--warning`, overdue/negative → `--error`/`--destructive`,
  informational/voided → `--info`. Surfaces use `bg-card`/`bg-background`,
  text uses `text-foreground`/`text-muted-foreground`, borders use `border-border`.
- **Accent.** This surface is **ERP · Timón**, so the accent is the LOCKED LCH Navy
  `#003A70` already in `--primary`; the surface consumes contract defaults with no
  override. The old off-palette green `#00843D` for "positive" is replaced by the
  shared `--success` teal the audit flagged.
- **Fonts.** All money/figures moved from `font-['JetBrains_Mono']` to `font-mono`
  (IBM Plex Mono); labels likewise (no more literal `font-['IBM_Plex_Mono']`).
  No JetBrains Mono, no Apax.
- **Theming.** Now `.dark`-aware purely via semantic tokens — no hard-coded light
  surfaces (`bg-white`, `bg-[#F4F7FA]`, `text-white`).
- **Naming / tenancy.** Dropped the `LchFinanzas*` component prefix → `KpiCard`,
  `DataTable`, `EstadoBadge`, `CurrencyInput`, `ExportBtn`; the surface is named for
  the app (`Pháros · Timón`), not the tenant.
- **Preserved unchanged:** audience (admin/finance team), surface purpose (finance
  ERP), the component inventory, the COP/`Intl.NumberFormat` + `DD/MM/YYYY`
  formatting logic, and the currency/KPI/table UX patterns.
