  $ git init --quiet
  $ mkdir sub
  $ mkdir sub/another
  $ echo notreallymusic >sub/another/jam.mp3
  $ sha1sum sub/another/jam.mp3
  477b00ed50e036d8a8a367012f994e7227b001df  sub/another/jam.mp3
  $ big add sub/another/jam.mp3
  $ stat --format='%F %N' sub/another/jam.mp3
  symbolic link `sub/another/jam.mp3' -> `.big/47/7b00ed50e036d8a8a367012f994e7227b001df.data'
  $ stat --format='%F %N' sub/another/.big
  symbolic link `sub/another/.big' -> `../../.git/big'
  $ cat .git/big/47/7b00ed50e036d8a8a367012f994e7227b001df.data
  notreallymusic
  $ cat sub/another/jam.mp3
  notreallymusic
