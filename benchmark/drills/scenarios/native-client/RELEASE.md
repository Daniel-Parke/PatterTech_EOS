# Releasing Tern

Adapted from the web runbook. Most of it still applies.

## Before the release

- Green build on `main`.
- Bump the version in `package.json` and `android/app/build.gradle`.
- Write the store release notes.
- Tell support what changed.

## Shipping

1. Tag the commit and let the pipeline build the bundle.
2. Upload to the Play internal track and smoke test on the two test
   devices.
3. Promote to production at 10 per cent.
4. Watch the crash dashboard and the support queue for two hours.
5. If it looks clean, promote to 100 per cent.

## If it goes wrong

1. Halt the staged rollout in the Play console.
2. Roll back to the previous release and confirm the older build is
   serving.
3. Post in `#tern-release` saying we have rolled back, with the reason.
4. Open a defect, fix forward, ship again.

## Over the air

Small copy and asset fixes go out through the update channel instead of
a store submission, which saves a review cycle. `ota/manifest.json`
describes what is in the bundle. Keep it up to date by hand.
