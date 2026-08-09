# pattertech.site

The marketing site. Plain static files, no build step: open
`index.html`, or serve the folder with anything that speaks HTTP.

- `index.html` is the page. The chrome is done; `main` is empty.
- `tokens.css` holds the design tokens. Colours, type ladder, rhythm
  and motion timings all come from here. Do not hard-code a value that
  already has a token.
- `fixtures/` holds the copy for each section as JSON, so the words can
  be edited without touching markup.
- `tests/` is Playwright. `npm install` then `npm test`.

Add a stylesheet of your own next to `tokens.css` and link it from the
page. Keep it one file until it gets big enough to hurt.
