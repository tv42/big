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
  $ sha1sum jam.mp3
  477b00ed50e036d8a8a367012f994e7227b001df  jam.mp3
  $ stat --format='%F %N' jam.mp3
  symbolic link `jam.mp3' -> `.big/47/7b00ed50e036d8a8a367012f994e7227b001df.data'
  $ stat --format='%F %N' .big
  symbolic link `.big' -> `.git/big'
  $ stat --format='%F %A' .git/big
  directory drwxr-xr-x
  $ stat --format='%F %A' .git/big/47/7b00ed50e036d8a8a367012f994e7227b001df.data
  regular file -r--r--r--
  $ cat .git/big/47/7b00ed50e036d8a8a367012f994e7227b001df.data
  notreallymusic
