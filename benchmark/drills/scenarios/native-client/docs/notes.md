# Working notes

Kept loosely. Whatever is here was true when it was written.

## Sync

The demo used one device, so none of the two-device questions came up.
They do now. Sam had two phones in the standup and the booking screen
let both of them hold the nine o'clock slot; whoever's phone reconnected
second ended up with it, and the other person was never told.

Someone suggested we pull in a CRDT library and be done. Alex pushed
back: it would make the notes lovely and would do nothing sensible with
a slot that only one person can have.

## Outbox

In memory. Known. `pending()` is there so a test can see the queue.

## Stub server

`stall()` stops it answering so we can reproduce the hotel-wifi case.
Nothing uses it yet. Last time we tried it by hand the app sat on the
spinner until it was force quit.

## Accessibility

Nothing formal. Priya ran TalkBack over the list screen and said the add
button announces as "button" with no name, because it is an icon and
nothing else, and the little wave graphic in the header gets read out as
an unnamed image for no reason. Same on the detail screen: the note
field announces as "edit box" and the placeholder is not a name. The
theme switch is a switch with nothing attached to it. The rule of thumb
she left us is that anything you can press needs a name, and anything
that is only decoration needs saying so.

## Store account

Play console is live. Apple is still in verification.
