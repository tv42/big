  $ git init --quiet
  $ mkdir sub
  $ cd sub
  $ mkdir another
  $ echo notreallymusic >another/jam.mp3
  $ sha1sum another/jam.mp3
  477b00ed50e036d8a8a367012f994e7227b001df  another/jam.mp3
  $ big add another/jam.mp3
  $ stat --format='%F %N' another/jam.mp3
  symbolic link 'another/jam.mp3' -> '.big/47/7b00ed50e036d8a8a367012f994e7227b001df.data'
  $ stat --format='%F %N' another/.big
  symbolic link 'another/.big' -> '../../.big'
  $ stat --format='%F %N' ../.big
  symbolic link '../.big' -> '.git/big'
  $ cat another/jam.mp3
  notreallymusic
