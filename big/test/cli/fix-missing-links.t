  $ umask 0022
  $ git init --quiet
  $ echo notreallymusic >jam.mp3
  $ sha1sum jam.mp3
  477b00ed50e036d8a8a367012f994e7227b001df  jam.mp3
  $ big add jam.mp3
  $ rm .big
  $ cat jam.mp3
  cat: jam.mp3: No such file or directory
  [1]
  $ big fix-missing-links jam.mp3
  $ cat jam.mp3
  notreallymusic
