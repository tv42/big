  $ umask 0022
  $ mkdir one
  $ cd one
  $ git init --quiet
  $ touch .gitignore
  $ git add .gitignore
  $ git commit --quiet -m 'Initial import.'
  $ cd ..
  $ git clone --quiet one two
  $ cd two
  $ echo notreallymusic >jam.mp3
  $ big add jam.mp3
# TODO "big add" should do "git add" too
  $ git add jam.mp3
  $ git commit --quiet -m 'Import some jams.'
  $ stat --format='%F %N' jam.mp3
  symbolic link 'jam.mp3' -> '.big/47/7b00ed50e036d8a8a367012f994e7227b001df.data'
  $ test ! -e ../one/.git/big && echo 'not there yet'
  not there yet
  $ big put origin jam.mp3
  $ stat --format='%F %A' ../one/.git/big/47/7b00ed50e036d8a8a367012f994e7227b001df.data
  regular file -r--r--r--
  $ cat ../one/.git/big/47/7b00ed50e036d8a8a367012f994e7227b001df.data
  notreallymusic

  BORK
