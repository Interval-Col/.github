// Wraps @iconify/tailwind for use with Tailwind v4's @plugin directive.
// @iconify/tailwind exports named functions only; @plugin requires a default export.
const plugin = require("tailwindcss/plugin");
const { addDynamicIconSelectors } = require("@iconify/tailwind");

const iconifyPlugin = addDynamicIconSelectors();
module.exports = plugin(iconifyPlugin.handler, iconifyPlugin.config || {});
