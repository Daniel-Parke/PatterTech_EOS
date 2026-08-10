# Deploys

One deployable, three boxes, a load balancer in front. We host it and
run it; nothing leaves the building as a package, a binary or a tarball,
and there is no customer install to think about. If that ever changes it
changes a lot of things, so it would be a conversation first.

## The steps

1. `make test` and `make scan` locally, both green.
2. Tag it: `git tag -a v0.4.x -m "..."`.
3. `ops deploy postbox v0.4.x`, which pulls the tag onto box one, drains
   it, restarts, and moves on when `/health` comes back.

## The build boxes

No outbound network. Dependencies come from `vendor/`, which the nightly
index sync refreshes from the internal mirror. If something you need is
not in there, ask in #platform and it gets added to the mirror first.

## Data

`data/` on each box holds the JSON stores. Backed up nightly to the
office NAS and kept for thirty days. It is not in the repository and
must never be.
