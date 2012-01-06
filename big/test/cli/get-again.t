  $ umask 0022
  $ mkdir one
  $ cd one
  $ git init --quiet
  $ echo notreallymusic >jam.mp3
  $ big add jam.mp3
# TODO "big add" should do "git add" too
  $ git add jam.mp3
  $ git commit --quiet -m 'Import some jams.'
  $ cd ..
  $ git clone --quiet one two
  $ cd two
  $ stat --format='%F %N' jam.mp3
  symbolic link `jam.mp3' -> `.big/47/7b00ed50e036d8a8a367012f994e7227b001df.data'
  $ cat jam.mp3
  cat: jam.mp3: No such file or directory
  [1]
  $ test ! -e .big && echo 'not there yet'
  not there yet
  $ big get jam.mp3
  $ cat jam.mp3
  notreallymusic
  $ stat --format='%F %N' jam.mp3
  symbolic link `jam.mp3' -> `.big/47/7b00ed50e036d8a8a367012f994e7227b001df.data'
# TODO implement "big drop"
  $ rm .big/47/7b00ed50e036d8a8a367012f994e7227b001df.data
  $ big get jam.mp3
  $ cat jam.mp3
  notreallymusic
