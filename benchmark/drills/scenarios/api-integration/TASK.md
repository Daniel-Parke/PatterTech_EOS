# Change request: orders API, sprint 24

Four changes to the orders API, all wanted for the same release.

## 1. Rename the order reference field

`orders[].ref` is a bad name. Product and support both call it the
reference. Rename it to `orders[].reference` in the API.

## 2. Currency on the create request

Every order today is assumed to be in GBP. We are opening the Irish
store in September, so the create request needs a `currency` field and
it must be supplied, not guessed.

## 3. Cursor pagination on GET /orders

`GET /orders` pages with `limit` and `offset`. The warehouse tool walks
the whole list every ten minutes and keeps seeing duplicates when new
orders land mid walk. Move it to a cursor.

## 4. The payment webhook must verify signatures

The provider signs every event. We do not check the signature, we check
a shared token that has been in the repo since the first release. The
provider sends:

    X-Webhook-Signature: hex sha256 HMAC of "<timestamp>.<raw body>"
    X-Webhook-Timestamp: unix seconds

The signing secret is in `WEBHOOK_SECRET`. Their docs say to reject an
event whose timestamp is too far from now, so that a captured request
cannot be replayed later.

## Notes

The warehouse picking tool is on a six week release train and the
storefront client ships weekly. Neither will be rebuilt for this
release.
