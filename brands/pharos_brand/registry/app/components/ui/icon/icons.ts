// Curated Pháros icon registry — the "Lucide + Material Symbols subset" the
// <Icon> wrapper renders (RFC 0008 icon standard, Phase 1.4).
//
// This list IS the safelist. The <Icon> wrapper builds the Iconify classes at
// RUNTIME, which Tailwind's source scan can't see — so every id here is
// force-generated via the `@source inline(…)` block in app/assets/css/main.css.
// KEEP THE TWO IN SYNC: an id added here must be added there, or it renders blank.
//
// Lucide is the house set; Material Symbols (outline) covers clinical glyphs
// Lucide lacks. ids use the `prefix--name` form @iconify/tailwind expects.

export const ICONS = {
  // ── Lucide (house set) ──
  search: 'lucide--search',
  check: 'lucide--check',
  close: 'lucide--x',
  add: 'lucide--plus',
  edit: 'lucide--pencil',
  delete: 'lucide--trash-2',
  user: 'lucide--user',
  users: 'lucide--users',
  calendar: 'lucide--calendar',
  clock: 'lucide--clock',
  phone: 'lucide--phone',
  mail: 'lucide--mail',
  settings: 'lucide--settings',
  chevronDown: 'lucide--chevron-down',
  chevronRight: 'lucide--chevron-right',
  selector: 'lucide--chevrons-up-down',
  back: 'lucide--arrow-left',
  filter: 'lucide--filter',
  download: 'lucide--download',
  upload: 'lucide--upload',
  print: 'lucide--printer',
  info: 'lucide--info',
  warning: 'lucide--triangle-alert',
  success: 'lucide--circle-check',
  error: 'lucide--circle-x',
  alert: 'lucide--circle-alert',
  refresh: 'lucide--refresh-cw',
  view: 'lucide--eye',
  file: 'lucide--file-text',
  home: 'lucide--house',
  logout: 'lucide--log-out',
  menu: 'lucide--menu',
  spinner: 'lucide--loader-circle',
  // ── Material Symbols (clinical subset — outline) ──
  patient: 'material-symbols--patient-list-outline',
  stethoscope: 'material-symbols--stethoscope-outline',
  labs: 'material-symbols--labs-outline',
  vaccine: 'material-symbols--vaccines-outline',
  syringe: 'material-symbols--syringe-outline',
  medical: 'material-symbols--medical-services-outline',
  prescription: 'material-symbols--prescriptions-outline',
  bloodType: 'material-symbols--bloodtype-outline',
  vitals: 'material-symbols--monitor-heart-outline',
  clinicalNotes: 'material-symbols--clinical-notes-outline',
  emergency: 'material-symbols--emergency-outline',
  glucose: 'material-symbols--glucose-outline',

  // ── Lucide — admission-patient coverage (icon cross-check, all verified) ──
  slidersHorizontal: 'lucide--sliders-horizontal',
  ambulance: 'lucide--ambulance',
  anchor: 'lucide--anchor',
  undo: 'lucide--undo',
  arrowRight: 'lucide--arrow-right',
  ban: 'lucide--ban',
  bell: 'lucide--bell',
  building: 'lucide--building',
  calendarCheck: 'lucide--calendar-check',
  calendarDays: 'lucide--calendar-days',
  calendarPlus: 'lucide--calendar-plus',
  calendarReschedule: 'lucide--calendar-arrow-up',
  calendarX: 'lucide--calendar-x',
  click: 'lucide--mouse-pointer-click',
  clockPlus: 'lucide--clock-plus',
  copy: 'lucide--copy',
  door: 'lucide--door-open',
  moreVertical: 'lucide--ellipsis-vertical',
  moreHorizontal: 'lucide--ellipsis',
  grid: 'lucide--grid-3x3',
  lockOpen: 'lucide--lock-open',
  rotate: 'lucide--rotate-cw',
  run: 'lucide--play',
  table: 'lucide--table',
  variable: 'lucide--variable',
  wand: 'lucide--wand',
  waves: 'lucide--waves',
  currency: 'lucide--dollar-sign',
  mapPin: 'lucide--map-pin',
  moon: 'lucide--moon',
  sun: 'lucide--sun',
  userRound: 'lucide--user-round',
  usersRound: 'lucide--users-round',
  panelLeft: 'lucide--panel-left',
  clipboardList: 'lucide--clipboard-list',
  banknote: 'lucide--banknote',
  radar: 'lucide--radar',
  queue: 'lucide--users-round', // reception queue metaphor (orphan → Lucide substitute)
  waitingRoom: 'lucide--hourglass', // waiting-room (orphan → Lucide substitute)
  timeExpired: 'lucide--alarm-clock-off', // cancelled/expired time (orphan → substitute)
  appWindow: 'lucide--app-window', // generic application (orphan → substitute)

  // ── Material Symbols — admission-patient clinical/UI coverage (verified) ──
  calendarBusy: 'material-symbols--event-busy-outline',
  receipt: 'material-symbols--receipt-outline',
  heartbeat: 'material-symbols--cardiology-outline',
  lungs: 'material-symbols--respiratory-rate-outline',
  microscope: 'material-symbols--science-outline',
  apps: 'material-symbols--apps',
  manageAccounts: 'material-symbols--manage-accounts-outline',
  sort: 'material-symbols--sort',
} as const

export type IconName = keyof typeof ICONS

export interface IconEntry {
  name: IconName
  id: string
  collection: 'lucide' | 'material-symbols'
}

/** Flat list for the catalog / discovery surface. */
export const ICON_LIST: IconEntry[] = (Object.entries(ICONS) as [IconName, string][]).map(
  ([name, id]) => ({
    name,
    id,
    collection: id.startsWith('material-symbols') ? 'material-symbols' : 'lucide',
  }),
)
