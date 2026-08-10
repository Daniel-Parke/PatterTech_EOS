# vendor

Wheels from the internal index, unpacked into the tree because the
build boxes have no network. The snapshot is everything the index
holds, not only what this service uses; `requirements.txt` says what we
actually pin.

The `.dist-info` directories come out of the wheels as they were built.
Do not edit them by hand: the next sync overwrites them.
