// Tests for the pure half of MapaBase (brands/pharos_brand/registry/app/lib/mapa.ts).
// Synthetic data only. Runs on Node ≥ 23.6 (TypeScript type stripping on by default):
//   node --test scripts/test_mapa_lib.mjs
import assert from 'node:assert/strict'
import { test } from 'node:test'
import {
  PROP_ID, PROP_VALOR, conAlfa, cortes, esExterna, estilo, expresionRelleno, filasTabla, normalizarCoropletas, rampa, rgb, valorDe,
} from '../brands/pharos_brand/registry/app/lib/mapa.ts'

const f = (id, props) => ({ type: 'Feature', id, properties: props, geometry: null })

test('valorDe: numbers, numeric strings, and nothing else', () => {
  assert.equal(valorDe(f(1, { v: 3 }), 'v'), 3)
  assert.equal(valorDe(f(1, { v: '4.5' }), 'v'), 4.5)
  for (const v of [null, undefined, '', 'x', NaN, Infinity]) assert.equal(valorDe(f(1, { v }), 'v'), null)
  assert.equal(valorDe(f(1, null), 'v'), null)
})

test('cortes: square-root classes, ascending, no duplicates, empty-safe', () => {
  assert.deepEqual(cortes([], 5), [])
  assert.deepEqual(cortes([0, 0], 5), [])
  const c = cortes([1, 10, 100], 5)
  assert.equal(c.length, 4)
  assert.ok(c.every((x, i) => i === 0 || x > c[i - 1]))
  assert.equal(c[0], 4) // (1/5)² × 100: one dense zone does not swallow the low classes
  assert.deepEqual(cortes([null, -3, 50], 2), [12.5])
})

test('rgb and rampa: from the background token to the series token', () => {
  assert.deepEqual(rgb('#fff'), [255, 255, 255])
  assert.deepEqual(rgb('rgb(0, 58, 112)'), [0, 58, 112])
  assert.equal(rgb('oklch(0.5 0.1 200)'), null)
  const r = rampa('#ffffff', '#000000', 4)
  assert.equal(r.length, 4)
  assert.notEqual(r[0], 'rgb(255, 255, 255)') // the first class is a visible tint, never the background
  assert.equal(r[3], 'rgb(0, 0, 0)')
  assert.deepEqual(rampa('nope', '#123456', 3), ['#123456', '#123456', '#123456'])
})

test('conAlfa keeps the hue', () => {
  assert.equal(conAlfa('#003a70', 0), 'rgba(0, 58, 112, 0)')
  assert.equal(conAlfa('nope', 0.5), 'nope')
})

test('filasTabla: same figures as the map, sorted by value, nulls last', () => {
  const fc = { type: 'FeatureCollection', features: [f('a', { n: 'A', v: 2 }), f('b', { n: 'B', v: null }), f('c', { n: 'C', v: 9 })] }
  assert.deepEqual(filasTabla(fc, 'v', 'n').map((x) => [x.id, x.valor]), [['c', 9], ['a', 2], ['b', null]])
  assert.deepEqual(filasTabla(null, 'v', 'n'), [])
})

test('esExterna: relative and same-origin pass, anything else is external', () => {
  assert.equal(esExterna('/analitica/api/mapa/base.pmtiles'), false)
  assert.equal(esExterna('https://tiles.example.org/x.pmtiles'), true)
  assert.equal(esExterna('//cdn.example.org/x'), true)
  assert.equal(esExterna('http://app.example.test/mapa.pmtiles', 'http://app.example.test'), false)
  assert.equal(esExterna('http://app.example.test.evil.example/x', 'http://app.example.test'), true)
  assert.equal(esExterna(undefined), false)
})

test('esExterna: the browser reads a backslash as a slash, so the guard must too', () => {
  const app = 'https://app.example.test'
  for (const u of ['https:\\\\evil.example/x.pmtiles', '/\\evil.example/x.pmtiles', '\\\\evil.example/x', ' //evil.example/x', 'ftp://evil.example/x', 'data:text/plain,x']) {
    assert.equal(esExterna(u, app), true, u)
    assert.equal(esExterna(u), true, u)
  }
  assert.equal(esExterna('https://app.example.test:8443/x', app), true)  // another port is another origin
  assert.equal(esExterna('https://app.example.test/x/y.pmtiles', app), false)
  assert.equal(esExterna('mapa/base.pmtiles', app), false)
  assert.equal(esExterna('/glyphs/{fontstack}/{range}.pbf', app), false)
})

test('normalizarCoropletas: the map paints and selects what the table shows', () => {
  const fc = { type: 'FeatureCollection', features: [
    { type: 'Feature', id: 'zona-a', properties: { n: 10 }, geometry: null },
    { type: 'Feature', properties: { id: 'zona-b', n: '' }, geometry: null },
    { type: 'Feature', properties: { n: 'abc' }, geometry: null },
  ] }
  const f = normalizarCoropletas(fc, 'n').features
  assert.deepEqual(f.map((x) => x.properties[PROP_VALOR]), [10, null, null])  // "" is suppressed, never 0
  assert.deepEqual(f.map((x) => x.properties[PROP_ID]), ['zona-a', 'zona-b', '2'])
  assert.deepEqual(filasTabla(fc, 'n', 'n').map((x) => x.id).sort(), ['2', 'zona-a', 'zona-b'])  // same ids as the table
  assert.equal(fc.features[0].properties[PROP_VALOR], undefined)  // the caller's data stays untouched
})

test('estilo: nothing external by default, and an external URL throws', () => {
  const s = estilo({ fondo: '#fff' })
  assert.deepEqual(s.sources, {})
  assert.equal(s.glyphs, undefined)
  assert.equal(s.sprite, undefined)
  assert.equal(JSON.stringify(s).includes('http'), false)
  assert.throws(() => estilo({ fondo: '#fff', origen: { url: 'https://tiles.example.org/a.pmtiles' } }), /RFC 0043 R2/)
  assert.throws(() => estilo({ fondo: '#fff', origen: { url: '/a.pmtiles', glyphs: 'https://fonts.example.org/{fontstack}/{range}.pbf' } }), /glyphs/)
  const ok = estilo({ fondo: '#fff', origen: { url: '/a.pmtiles' }, capasBase: [{ id: 'x' }] })
  assert.equal(ok.sources.base.url, 'pmtiles:///a.pmtiles')
  assert.equal(ok.layers.length, 2)
})

test('expresionRelleno: null values are transparent, steps follow the breaks', () => {
  const e = expresionRelleno('v', [10, 20], ['c0', 'c1', 'c2'])
  assert.equal(e[0], 'case')
  assert.equal(e[2], 'rgba(0,0,0,0)')
  assert.deepEqual(e[3].slice(2), ['c0', 10, 'c1', 20, 'c2'])
})
