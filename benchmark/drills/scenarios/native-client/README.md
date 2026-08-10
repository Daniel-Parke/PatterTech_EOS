# Tern

A single-surface task client. One list, one detail sheet, one booking
screen, one settings screen. React Native, Android first, iOS to follow
once the store account clears.

Everything is written locally first and pushed to the server when the
device has a network. People use this on trains and in basements, so
"when the device has a network" can mean tomorrow.

## Layout

- `src/core/` the offline engine. `index.js` is the surface the app and
  the tests use; nothing outside `src/core/` reaches past it.
  - `state.js` the state shape and `canonical()`, a stable serialiser we
    use whenever two states have to be compared.
  - `store.js` the local store, a JSON file under the app's data
    directory.
  - `outbox.js` the queue of writes waiting to go to the server.
  - `sync.js` `createClient()`, plus `applyOp()`, which is the only
    place a write changes state.
  - `flags.js` reads `src/config/flags.json`.
- `src/server/stub.js` the stub server we develop against. It can be
  told to stall so we can see what the client does when an
  acknowledgement never arrives.
- `src/screens/` the four screens.
- `android/` the native project. `ota/` the update channel.

## Write classes

Three, and they do not behave alike.

- `notes` free text on a task. Two people editing the same note at the
  same time is normal and expected.
- `preferences` one value per user per key. Theme, sort order, reminder
  time.
- `bookings` a slot in the shared calendar. A slot is held by exactly
  one person.

## Running it

```
npm install
npm run android
```

Tests: `npm test` (that is `node --test`; the core has no dependencies
and runs on plain Node).

## Known state

This is the prototype we demoed, tidied up. It works when the network is
there.

- `applyOp()` applies whatever arrives in the order it arrives. Nobody
  has decided what should happen per write class, so the answer today is
  "whatever the server saw last".
- The outbox is in memory. Kill the app with writes queued and they are
  gone.
- `flush()` awaits the server. If the server never answers, it never
  returns, and the screen keeps showing the spinner.
- The release runbook is the one we wrote for the web product, lightly
  edited.
- `ota/manifest.json` is hand-maintained and nothing compares it to what
  the binary actually ships.
