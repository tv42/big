  $ echo not-stored-big >deceiving-example
  $ big get deceiving-example
  big get: deceiving-example: Not a big file (not a symlink)
  [1]

  $ ln -s not-stored-big-either link-to-other
  $ big get link-to-other
  big get: link-to-other: Not a big file
  [1]
