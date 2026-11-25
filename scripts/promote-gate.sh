#!/usr/bin/env bash
# Aviso del promote: dice en el PR develop → main qué se lleva que alguien marcó como no listo.
#
#   (a) PR mergeados con la etiqueta `bloquea-promote` que están en la cabeza del PR y no en la base.
#   (b) Casillas sin marcar en la sección «Antes de mergear» del cuerpo del PR.
#
# Por defecto solo avisa (ENFORCE=false): el promote se lleva todo develop, así que bloquearlo
# frenaría también a quien sí necesita desplegar. Lo que no está listo entra apagado detrás de
# una bandera (BRANCHING-AND-DEPLOY.md §Lo que no está listo entra apagado).
#
# Variables: REPO, HEAD_SHA, BASE_REF, y PR o PR_BODY_FILE (este último para probar en local).
# Opcionales: LABEL (default bloquea-promote), ENFORCE (default false).
# Si la API o git fallan, el job falla: un aviso que no se pudo calcular no se da por bueno.
set -euo pipefail

LABEL="${LABEL:-bloquea-promote}"
ENFORCE="${ENFORCE:-false}"
SUMMARY="${GITHUB_STEP_SUMMARY:-/dev/stdout}"
findings=()

# Los comandos de workflow interpretan % y saltos de línea; se escapan para que el texto
# del PR no se lea como otro comando.
escape() { local s="${1//'%'/'%25'}"; s="${s//$'\r'/}"; printf '%s' "${s//$'\n'/'%0A'}"; }

# (a) Sin --base: cuenta también un PR apilado sobre otra rama; lo que decide es la ascendencia.
labeled=$(gh pr list --repo "$REPO" --state merged --label "$LABEL" --limit 200 \
  --json number,title,mergeCommit \
  --jq '.[] | select(.mergeCommit != null) | [.number, .mergeCommit.oid, .title] | @tsv')

while IFS=$'\t' read -r number sha title; do
  [ -n "$number" ] || continue
  # Exit 1 = no es ancestro; 128 = el commit no está en el clon, así que tampoco está en la cabeza.
  if git merge-base --is-ancestor "$sha" "$HEAD_SHA" 2>/dev/null \
     && ! git merge-base --is-ancestor "$sha" "origin/$BASE_REF"; then
    findings+=("#$number $title — tiene la etiqueta «$LABEL»")
  fi
done <<< "$labeled"

# (b) El cuerpo se lee en vivo: al volver a correr el job, el del evento es el viejo.
if [ -n "${PR_BODY_FILE:-}" ]; then
  body=$(cat "$PR_BODY_FILE")
else
  body=$(gh api "repos/$REPO/pulls/$PR" --jq '.body // ""')
fi

while IFS= read -r box; do
  [ -n "$box" ] && findings+=("Casilla sin marcar: $box")
done < <(printf '%s\n' "$body" | tr -d '\r' | awk '
  /^#+[[:space:]]/ { inside = ($0 ~ /[Aa]ntes de mergear/); next }
  inside && sub(/^[[:space:]]*[-*][[:space:]]+\[[[:space:]]\][[:space:]]*/, "") { print }')

if [ ${#findings[@]} -eq 0 ]; then
  echo "✓ El promote no lleva nada marcado como no listo."
  exit 0
fi

{
  echo "### Este promote lleva algo marcado como no listo para prod"
  echo
  for f in "${findings[@]}"; do echo "- $f"; done
  echo
  echo "Si eso ya está apagado detrás de una bandera, puede salir. Si no, quien lo hizo lo apaga,"
  echo "o quita la etiqueta y marca la casilla cuando ya esté listo."
} >> "$SUMMARY"

for f in "${findings[@]}"; do
  if [ "$ENFORCE" = "true" ]; then echo "::error::$(escape "$f")"; else echo "::warning::$(escape "$f")"; fi
done

[ "$ENFORCE" = "true" ] && exit 1
exit 0
