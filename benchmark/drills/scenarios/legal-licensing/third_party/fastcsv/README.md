# fastcsv

Copied out of https://github.com/hollowbit/fastcsv at commit 9f2c1ab on
2 November 2025 and trimmed to the two functions we use. It is quicker
than the standard library on the wide exports and it quotes the way the
finance spreadsheet wants, which the standard library will not do.

Changes: deleted the reader, deleted the numpy path, kept the writer.

Nobody has looked at this since. If it starts misbehaving on a big
export, the upstream project has moved on a long way.
