====================
 Think Big, Git Big
====================

Large file storage with Git

``big`` extends git_ so it is able to handle large collections of
large files -- more than you'd have disk space for.

- only the files you request are available locally
- multiple copies are maintained for data integrity


``big`` is not like git-annex_, because

- it doesn't track the locations of the data files in the git
  repository
- it's not written in Haskell, so it might even work across
  distribution upgrades and platforms
- symlink destinations don't have to change when you move files from
  one directory to another
- it syncs over sftp, using Paramiko_

Much like git-annex_\ 's `"not" page
<http://git-annex.branchable.com/not/>`__ explains, ``big`` also
isn't

- a backup system (it does not keep history of the big files)
- filesystem (but you're free to fiddle with FUSE)
- not just a way to store large files; partial checkouts and replicas
  also matter a lot
- git-media_, because ``big`` does partial checkouts

``big`` exists because managing about 3TB of data with git-annex_
got too frustrating. We'll see if it's an actual improvement, or just
something fun to hack on.

.. _git: http://git-scm.org/
.. _git-annex: http://git-annex.branchable.com/
.. _git-media: https://github.com/schacon/git-media
.. _Paramiko: http://www.lag.net/paramiko/

