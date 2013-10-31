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
# shouldn't need to do anything
  $ big put origin jam.mp3

  BORK
