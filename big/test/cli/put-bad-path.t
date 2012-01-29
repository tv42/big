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
  $ big put origin does-not-exist
  big put: does-not-exist: No such file or directory
  [1]
