  $ git init --quiet
  $ mkdir sub
  $ cd sub
  $ echo notreallymusic >jam.mp3
  $ sha1sum jam.mp3
  477b00ed50e036d8a8a367012f994e7227b001df  jam.mp3
  $ big add jam.mp3
  $ stat --format='%F %N' jam.mp3
  symbolic link 'jam.mp3' -> '.big/47/7b00ed50e036d8a8a367012f994e7227b001df.data'
  $ stat --format='%F %N' .big
  symbolic link '.big' -> '../.big'
  $ stat --format='%F %N' ../.big
  symbolic link '../.big' -> '.git/big'
  $ cat jam.mp3
  notreallymusic
