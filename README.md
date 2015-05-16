Scramble
========

Scramble symlinks python packages into a folder.

This allows quick traversal to available modules during development.

Namespaced packages are symlinked together.

Installation
------------

pip install scramble


Running
-------

By default, scramble will symlink the packages available into a folder "scramble"

```
scramble
```

You can specify a different folder with the target option

```
scramble --target foo
```
