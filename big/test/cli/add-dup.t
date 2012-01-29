  $ umask 0022
  $ git init --quiet
  $ echo notreallymusic >jam.mp3
  $ sha1sum jam.mp3
  477b00ed50e036d8a8a367012f994e7227b001df  jam.mp3
  $ big add jam.mp3
  $ echo notreallymusic >another.mp3
  $ big add another.mp3
