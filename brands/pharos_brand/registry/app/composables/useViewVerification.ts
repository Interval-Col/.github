// El puente entre el vocabulario (registry) y el manifiesto (app).
//
// Vive acá, y no en `lib/verification.ts`, por una razón técnica que ya costó una
// regresión: `lib/verification.ts` lo importan serializadores HEADLESS (el
// `build-spec.ts` de design-studio, bajo jiti) donde el alias `~` de Nuxt NO resuelve.
// Un `import … from '~/verification.manifest'` allá rompe `pnpm regen-spec`, y ningún
// CI lo atrapa porque ese CLI necesita el checkout hermano del registry y solo corre en
// local. Acá no: `app/composables/**` es territorio de Nuxt y nada headless lo toca.
//
// Al vivir en composables/, Nuxt lo AUTO-IMPORTA: las páginas llaman
// `verificationFor(route.path)` sin importar nada.
import { VERIFICATION_MANIFEST } from '~/verification.manifest'
import { VERIFICATION_STATES, type ViewVerification } from '~/lib/verification'

/**
 * Estado de verificación de una ruta, leído del manifiesto de la app.
 * `undefined` = liberada / no aplica ⇒ la vista se renderiza sin marca alguna.
 */
export function verificationFor(path: string): ViewVerification | undefined {
  const v = VERIFICATION_MANIFEST[path]
  if (!v || !VERIFICATION_STATES[v.estado].renders) return undefined
  return v
}
