Scramble
========

Modern python environments tend to place the active packages in different places in the filesystem.

Scramble symlinks active python packages into a folder.

This allows quick traversal to available modules during development, and places namespaced packages into a logical filesystem.


Installation
------------

pip install scramble


Running
-------

By default, scramble will symlink the packages available into a folder "scrambled"


Run with the command:

```
scramble
```

You can specify a different folder with the target option

```
scramble --target foo
```

Build status
------------

[![Build Status](https://travis-ci.org/phlax/scramble.svg?branch=master)](https://travis-ci.org/phlax/scramble)