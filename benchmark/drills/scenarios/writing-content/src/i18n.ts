import en from "../locales/en.json";

type Catalogue = Record<string, string>;

const catalogues: Record<string, Catalogue> = { en };

let active = "en";

export function setLocale(code: string): void {
  if (catalogues[code]) {
    active = code;
  }
}

export function locale(): string {
  return active;
}

export function t(key: string): string {
  const catalogue = catalogues[active] ?? catalogues.en;
  const value = catalogue[key];
  if (value === undefined) {
    if (import.meta.env.DEV) {
      console.warn("missing copy for " + key);
    }
    return key;
  }
  return value;
}
