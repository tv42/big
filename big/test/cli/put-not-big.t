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
  $ echo not-stored-big >deceiving-example
  $ big put origin deceiving-example
  big put: deceiving-example: Not a big file (not a symlink)
  [1]

  $ ln -s not-stored-big-either link-to-other
  $ big put origin link-to-other
  big put: link-to-other: Not a big file
  [1]
