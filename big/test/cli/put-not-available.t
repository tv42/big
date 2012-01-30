  $ umask 0022
  $ mkdir one
  $ cd one
  $ git init --quiet
  $ echo notreallymusic >jam.mp3
  $ big add jam.mp3
# TODO "big add" should do "git add" too
  $ git add jam.mp3
  $ git commit --quiet -m 'Import some jams.'
# TODO implement "big drop"
  $ rm .big/47/7b00ed50e036d8a8a367012f994e7227b001df.data
  $ cd ..
  $ git clone --quiet one two
  $ cd two
# TODO implement "big drop"
  $ big put origin jam.mp3
  big put: jam.mp3: No local copy of big file
  [1]
