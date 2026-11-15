# <repo> — lo que un agente necesita saber de este repo

<!--
Plantilla del contrato de cada repo (RFC 0039 D4). Reglas:
- Máximo 200 líneas. El detalle va en docs/ (enlazado desde aquí) y la guía de una ruta
  concreta en .claude/rules/. El check `agents-md-check` de Interval-Col/.github lo mide.
- Lo leen TODOS los agentes, incluidos revisores externos como Codex: nada de secretos,
  IPs internas que no sean ya públicas en el mapa, ni valores de pacientes.
- Una línea que nació de un incidente se queda (corta). La historia del incidente va en docs/.
- Fecha en cada afirmación medida: «(medido 2026-10-25)».
Borra este comentario al llenarla.
-->

## Para qué existe

Una o dos frases: qué hace este repo, para quién, y en qué estado está (activo, en
migración, legado). Si es parte de un producto o RFC, el puntero.

## Tronco y ramas

- Tronco: `develop`. Toda rama sale de `origin/develop` y todo PR se abre con
  `gh pr create --base develop`; a `main` solo llegan promotes `develop → main`.
  (Un repo sin `develop` escribe `main`. El check lo compara con el remoto.)
- Merge siempre con merge commit (`--merge`), nunca `--squash`.

## Reglas que obligan a este repo

Una línea por cada RFC aceptada cuyo `target-repos` nombra este repo, escrita como
instrucción y con su número (RFC 0039 D4). Si la regla restringe código, se acompaña con su
portón `scripts/check-rfc-<NNNN>-<qué>`.

- RFC NNNN — <la regla, como instrucción>.

## Correr y probar

```bash
# instalar · levantar en local · correr las pruebas · lint
```

## Fronteras de datos

- ¿Toca PHI? ¿Qué esquema de la base compartida es suyo? ¿Quién más lo lee?
- Cambios de esquema, GRANTs y migraciones solo por un paso de despliegue revisado.

## Despliegue

Por dónde sale a producción (workflow, host, ambiente) y qué lo dispara.

## Trampas

- 🪤 Lo que ya mordió una vez, en una línea cada una, con su fecha.
