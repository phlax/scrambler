Scrambler
========

Modern python environments tend to place the active packages in different places in the filesystem.

Scrambler symlinks active python packages into a single folder.

This allows quick traversal to available modules during development, and places namespaced packages into a logical filesystem.

This package was inspired by [collective.recipe.omelette](https://github.com/collective/collective), but does not require
a buildout environment to run


Installation
------------

pip install scrambler


Running
-------

By default, scrambler will symlink the packages available into a folder "scrambled"


Run with the command:

```
scrambler
```

You can specify a different folder with the target option

```
scrambler --target foo
```

Build status
------------

[![Build Status](https://travis-ci.org/phlax/scrambler.svg?branch=master)](https://travis-ci.org/phlax/scrambler)