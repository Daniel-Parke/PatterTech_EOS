// Remote flags. The file is bundled with the build and overwritten by
// the config fetch on launch; if the fetch fails we keep what we have.

import config from "../config/flags.json" with { type: "json" };

export function flags() {
  return Object.assign({}, config);
}

export function flag(name) {
  return flags()[name] === true;
}
