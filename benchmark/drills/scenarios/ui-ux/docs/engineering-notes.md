# Engineering notes

Kept short on purpose. Longer decisions belong in their own file.

## The public page

Written in a fortnight in 2023 when the old phone line kept dropping
calls during the January freeze. It has had small fixes since and no
proper pass. The three fields are the three the control room actually
needs: postcode, what the caller can see, and a number to ring back.

Known rough edges nobody has had time for:

- the styles are a single file of hex values, copied from the brochure
  site, and the two do not quite match any more
- the form tells you what is wrong next to the field, so on a phone you
  can submit and see nothing change
- there is no check-your-answers step, so people ring back to ask what
  they sent

## The access widget

Bought in 2023 on a two-year deal after a complaint, on the promise
that it made the site compliant. It loads from the supplier's CDN and
adds a button in the corner. Nobody here has looked at it since and the
renewal is in the drawer somewhere.

## What the control room asked for

Ellen's team watch the leak queue on a wall screen during a burst.
During the storm in February they had four browser tabs open and were
reading numbers off a spreadsheet that Mo updated by hand. What they
said they wanted, in their words: "one screen that tells us whether we
are keeping up".

They are on the same locked-down machines as everyone else, so whatever
we build has to run from the same static build as the public page.

## Build

`tools/build.py` is the whole thing. It copies `web/` into `dist/`. It
was going to do more and never needed to.
