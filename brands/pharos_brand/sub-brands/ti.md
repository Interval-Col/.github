# Pháros · Tecnología — TI sub-brand *(glyph: «Submarino» / submarine)*

> **✅ RATIFICADO 2026-08-10** (@gczuluaga; cierra [rfcs#63](https://github.com/Interval-Col/rfcs/issues/63)).
> El nombre user-facing queda **igual al provisional** — «Pháros · Tecnología», frente a las
> candidatas TI / TIC / Informática — así que no hay barrido de renombre: la clase de tema
> `.theme-ti`, el glyph custom `Submarine` y el acento navy ya eran el contrato estable y no
> cambian. Añadida como sexta sub-marca en la revisión 2026-07-03 de RFC 0004
> ([rfcs#60](https://github.com/Interval-Col/rfcs/issues/60)); el rol de mínimo privilegio
> `audit` viene de RFC 0021. Locked facts only; deeper brand narrative is **TODO — author
> with @SKuger01**. Parent source: [`../BRAND.md`](../BRAND.md) · [`../BACKBONE.md`](../BACKBONE.md).

## 1. At a glance

```
SUB-BRAND          Pháros · Tecnología      (user-facing; glyph = Submarino/submarine, custom)
FUNCTIONAL NAME    Pháros TI                (RFC 0004 §2, rev. 2026-07-03)
USER-FACING NAME   Pháros · Tecnología      (RATIFICADO 2026-08-10 — cierra rfcs#63; sin cambios sobre el provisional)
MARITIME GLYPH     Submarino → glyph custom `Submarine` (no está en lucide — vendorizado)
DESCRIPTOR         TI · Administración de plataforma
PERSONA            Operador de plataforma (hoy ~3 personas: German, Yanna, Samuel)
TENANCY            Holding-level — administra la plataforma misma, no una empresa miembro
ACCENT (LOCKED)    Navy profundo #002A52 light / #7FB0E6 dark
ACCENT SPREAD      Neutro
PILOT LIGHT        #E4002B — SHARED family constant
WORDMARK           Fraunces, burgundy #782F40 — SHARED construction
```

## 2. Positioning

`Pháros TI` es la app de administración de plataforma — el operador de plataforma (~3 personas)
es la persona sin superficie propia hasta ahora: SSO, observabilidad de la migración ETL,
certificados y administración de servicios resolvían acceso cada uno por su lado (tokens
compartidos, túneles SSH, runbooks). No es una app de cara al paciente ni a un cliente; **no
administra los datos de una empresa miembro** de la holding — administra **la plataforma
misma** (RFC 0004 §2).

### Módulos (cinco)

- **Auditoría** — tablero de observabilidad agregada del gate PII sobre el audit hash-only
  (RFC 0021); su primer build estaba gateado en esta ratificación (rfcs#63).
- **Accesos y SSO** — ciclo de vida de usuarios, resets de 2FA, sesiones (las *definiciones* de
  permisos siguen en git, RFC 0012); pliega la superficie hoy en `sso-management`.
- **Migración ETL** — observabilidad de la migración COBOL → nucleus-db (cobertura,
  value-check, jobs, preflight); primer módulo adoptado, hoy solo por túnel.
- **Servicios y certificados** — operación de certificados (runbook CA de nucleus-db, vistas de
  expiración) y administración de servicios (pools IP de `queue-api`, cuentas de servicio, salud
  de runners).
- **Telefonía** — monitor de captura SMDR. **No** es el panel de estadísticas de llamadas — ese
  vive en Admisiones.

### Roles de mínimo privilegio

| Rol | Alcance | Fuente |
|---|---|---|
| `it_admin` | Operador amplio: SSO, ETL, certificados, servicios | RFC 0004 §2 |
| `audit` | Solo lectura, **únicamente** el tablero de Auditoría — observabilidad agregada del gate PII | RFC 0021 |

⚠️ `audit` **no** es subconjunto de `it_admin` — RFC 0021 lo define expresamente como un rol
distinto y separado de la administración de plataforma: "ver el gate" no implica "administrar
la plataforma". Un vigilante de cumplimiento se asigna `audit`, no `it_admin`.

## 3. Visual (overrides only)

- **Accent** `--primary` = navy profundo `#002A52` (light) / `#7FB0E6` (dark); status colours
  accent-independent (Q4). Clase de tema `theme-ti` (+ `.dark`), definida en
  `registry/tokens.css` (líneas 245-252).
- **Glyph** la «Submarino» — no existe en lucide, está **vendorizada** como glyph custom
  `Submarine` en `registry/app/lib/custom-glyphs.ts` (línea 15, exportado en `CUSTOM_GLYPHS`
  línea 40). El shell la resuelve **custom-first** (antes de caer a lucide) — quien implemente
  el lockup necesita saber esto, no es un glyph de librería.
- **Lockup** ver §Lockup a continuación.
- Everything else inherited unchanged from `../BRAND.md`.

### Lockup (contrato de sidebar)

El sidebar muestra **solo el logo Pháros** (marca compartida de la familia) y una etiqueta
descriptiva en mono. El acento de sub-marca **no** aparece como sub-nombre junto al logo.

| Elemento | Valor |
|---|---|
| Logo en sidebar | Solo logo Pháros (sin sub-nombre acento al lado) |
| Sublabel descriptivo | `TI · Administración de plataforma` (IBM Plex Mono, uppercase, tracked, muted) |
| Eco en breadcrumb | Sí — «Tecnología» aparece como primer nodo del breadcrumb |
| Glyph de app | «Submarino» → glyph custom `Submarine` (vendorizado, custom-first), tintado navy; identidad marítima vive en la marca, no en la palabra |

> Fuente: RFC 0004 rev. 2026-07-03 · `registry/spec/ti.md` (spec-version `311729e5`, ya con
> entrada en `spec/.implemented.json`).

## 4. Voice

Inherits the shared Pháros voice (Spanish-first, technically precise, warm, never alarmist).
Domain register: operador de plataforma — directo y técnico, sin la calidez que exige una
superficie de cara al paciente; copy de auditoría e incidentes nombra el estado con precisión,
sin suavizarlo. *(TODO — refine with @SKuger01.)*

## References

- [RFC 0004 — Pháros product portfolio](https://github.com/Interval-Col/rfcs/blob/main/0004-pharos-product-portfolio.md)
  §2 (rev. 2026-07-03) — la decisión de crear `Pháros TI`.
- [RFC 0008 — Pháros design system](https://github.com/Interval-Col/rfcs/blob/main/0008-pharos-design-system.md)
  — sistema de diseño, glyphs náuticos, contrato de lockup.
- [RFC 0021 — PHI audit observability](https://github.com/Interval-Col/rfcs/blob/main/0021-phi-audit-observability.md)
  — el rol `audit`.
- [rfcs#60](https://github.com/Interval-Col/rfcs/issues/60) — revisión que añade `Pháros TI`
  como sexta sub-marca · [rfcs#63](https://github.com/Interval-Col/rfcs/issues/63) —
  ratificación del nombre user-facing (2026-08-10).
- [`README.md`](README.md) — family index · [`../BRAND.md`](../BRAND.md) — shared spec.
- [`../registry/spec/ti.md`](../registry/spec/ti.md) — spec del registry.
