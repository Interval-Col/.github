// @ts-check
// TEMPLATE — copied verbatim into each app by the registry sync. Requires
// @nuxt/eslint + a prior `nuxt prepare` (which generates ./.nuxt/eslint.config.mjs).
// The sync OVERWRITES this file in the app.
import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt(
  {
    files: ['**/*.vue'],
    rules: {
      'vue/no-parsing-error': 'error',
      'vue/valid-template-root': 'error',
      // Cosmetic multi-line-attribute rules are OFF: Pháros apps are authored in
      // a deliberately compact style, and these rules' autofix reflows every
      // multi-attr tag to one-attr-per-line with broken indentation. Correctness
      // rules + the four design gates stay enforced.
      'vue/first-attribute-linebreak': 'off',
      'vue/max-attributes-per-line': 'off',
    },
  },
  // Auto-generated shadcn-vue UI components — relax stylistic rules
  {
    files: ['app/components/ui/**/*.vue'],
    rules: {
      'vue/require-default-prop': 'off',
    },
  },
  // Ignore openapi-ts generated output
  {
    ignores: ['app/lib/api/generated/**'],
  },
)
