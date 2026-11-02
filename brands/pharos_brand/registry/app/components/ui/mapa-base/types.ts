import type { MapaBaseOrigen, MapaFeatureCollection, Lonlat } from '@/lib/mapa'

export type { MapaBaseOrigen, MapaFeatureCollection, Lonlat }

/** Polygons coloured by a numeric property (aggregates only — RFC 0043 R4). */
export interface CapaCoropletas {
  datos: MapaFeatureCollection
  /** Property with the number (e.g. patients per km²). */
  valor: string
  /** Property with the human label of each zone (the table's first column). */
  etiqueta: string
  /** Classes of the scale. Default 5. */
  pasos?: number
}

/** A density surface over points, each weighted by a property (default 1). */
export interface CapaCalor {
  datos: MapaFeatureCollection
  peso?: string
}

/** Marked places (e.g. sites). Labelled only when the basemap brings glyphs. */
export interface CapaPuntos {
  datos: MapaFeatureCollection
  etiqueta: string
}
