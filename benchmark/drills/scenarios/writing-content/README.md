# Hartfield storefront

The checkout front end. React and TypeScript, built with Vite.

- `src/` is the app. `SignupForm.tsx` is the account step people hit
  after they put something in the basket.
- `locales/en.json` holds the copy as flat keys. English is the only
  language we ship today.
- `src/i18n.ts` is the lookup. It is about thirty lines and does what
  it says.

## Working on it

    npm install
    npm run dev

`npm run build` type checks and bundles. CI runs the same two commands
on every push.

## House rules

Copy lives in `locales/en.json`, not in the components. Keys are
`area.thing`, lower camel after the dot. Keep the tone plain and short.
