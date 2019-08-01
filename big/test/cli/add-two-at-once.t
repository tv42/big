  $ umask 0022
  $ git init --quiet
  $ echo notreallymusic >jam.mp3
  $ echo notmusiceither >groove.mp3
  $ sha1sum jam.mp3
  477b00ed50e036d8a8a367012f994e7227b001df  jam.mp3
  $ sha1sum groove.mp3
  d89802139f25443e90e3bb959b0001d83e2e6dff  groove.mp3
  $ big add jam.mp3 groove.mp3
  $ stat --format='%F %N' jam.mp3 groove.mp3
  symbolic link 'jam.mp3' -> '.big/47/7b00ed50e036d8a8a367012f994e7227b001df.data'
  symbolic link 'groove.mp3' -> '.big/d8/9802139f25443e90e3bb959b0001d83e2e6dff.data'
  $ stat --format='%F %A' .git/big/47/7b00ed50e036d8a8a367012f994e7227b001df.data
  regular file -r--r--r--
  $ stat --format='%F %A' .git/big/d8/9802139f25443e90e3bb959b0001d83e2e6dff.data
  regular file -r--r--r--
  $ cat .git/big/47/7b00ed50e036d8a8a367012f994e7227b001df.data
  notreallymusic
  $ cat jam.mp3
  notreallymusic
  $ cat .git/big/d8/9802139f25443e90e3bb959b0001d83e2e6dff.data
  notmusiceither
  $ cat groove.mp3
  notmusiceither
