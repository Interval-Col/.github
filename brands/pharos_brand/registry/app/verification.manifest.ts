// pharos-registry:keep
//
// MANIFIESTO DE VERIFICACIÓN — qué vista de ESTA app lleva la marca de PROT-SW-001.
//
// Este archivo es de la APP, no del registry. El sync lo copia UNA VEZ (al adoptar
// ViewVerification.vue) y después nunca lo vuelve a tocar: la marca `pharos-registry:keep`
// de la primera línea es lo que se lo prohíbe. Edítalo con confianza; un re-sync no
// se lo lleva por delante.
//
// ⚠️ QUÉ VA ACÁ NO LO DECIDE INGENIERÍA. Qué vista está en qué estado, y quién responde
// por su verificación, lo deciden Calidad y Dirección Médica — no se deduce leyendo el
// código. Este archivo es donde esa decisión queda escrita y revisable en un PR.
//
// Reglas que el gate `check-view-verification.mjs` hace cumplir en CI:
//
//   1. Cada ruta acá tiene que existir como página.
//   2. Cada ruta acá tiene que montar <ViewVerification> en su página — si no, el
//      manifiesto afirma una marca que el usuario NO ve.
//   3. Y al revés: un <ViewVerification> sin entrada acá es una banda que nadie puede
//      auditar ni retirar.
//   4. `responsable` va NOMBRE + CARGO. Nunca un @handle ni un usuario técnico
//      (`SOP-000` §4): «responsable: @alguien» no le sirve al auditor ni a la persona
//      del mesón.
//   5. `no-conforme-acotado` EXIGE `restriccion` (`PROT-SW-001` §6.1).
//   6. `revisarAntes` es OBLIGATORIA y, si queda atrás, ROMPE EL BUILD. Una marca sin
//      caducidad se vuelve mobiliario: sigue en pantalla mucho después de dejar de ser
//      cierta, y ahí la gente deja de leerla — peor que no tenerla. El arreglo es que
//      Calidad mueva la fecha en un PR.
//   7. CERO datos de paciente (`PROT-SW-001` §8). Ni de ejemplo.
//   8. Si este manifiesto no está vacío, el layout tiene que montar
//      <ViewVerificationMark> — si no, hay banda pero no aviso ANTES de entrar.
//
// Cómo se marca una vista, en dos pasos:
//
//   a) Agrega su entrada acá.
//   b) Envuelve la vista, en su página:
//
//        <ViewVerification :v="verificationFor(route.path)">
//          <!-- la vista, tal como está -->
//        </ViewVerification>
//
// Quitar la marca = borrar la entrada. La página puede quedarse envuelta: sin entrada,
// el componente renderiza el contenido intacto. (Aun así el gate pide quitar el
// envoltorio, para que un `grep` diga la verdad sobre qué vistas están marcadas.)
import type { ViewVerification } from '~/lib/verification'

export const VERIFICATION_MANIFEST: Record<string, ViewVerification> = {
  // Ejemplo — bórralo y pon las vistas reales de esta app:
  //
  // '/resultados/liberacion': {
  //   estado: 'en-verificacion',
  //   responsable: { nombre: 'Sara Morales', cargo: 'Coordinación de Calidad' },
  //   protocolo: 'PROT-SW-001',
  //   expediente: 'FOR-SW-001 · entrega 2026-08',
  //   desde: '2026-08-04',
  //   revisarAntes: '2026-09-15',
  // },
}
