# Note

## Install

For '.rpm' based linux:  `yum install pandoc`.

For '.deb' based linux:  `apt install pandoc`.

Get the source and install:
```bash
$ cd
$ mkdir app
$ cd app
$ git clone <url>
$ cd note
$ ./install.sh
```
This installs to `~/.local/bin`.  Make sure that directory is in your PATH.


## Usage

Create a directory to hold your notes, and in it, make a file named `.noteignore`.
```bash
$ mkdir note-hobby
$ touch note-hobby/.noteignore
```

In the directory you created, create a file tree of your notes, like this example:
```
note-hobby/
    .noteignore
    rc-plane/
        hobby-zone-champ.md
        hobby-zone-sport-cub-s.md
        umx-radian.md
        delta-ray.md
    food/
        lasagna.md
        brats-n-kraut.md
        brown-butter.md
```

### Build

Navigate to anywhere inside `note-hobby/`, then do:
```
$ note build
```
Then `note` will convert your files to an html tree in `.build/`.
Navigate your browser to `file:///.../.build/index.html`.


### Clean

Navigate to anywhere inside `note-hobby/`, then do:
```
$ note clean
```
Then `note` will delete the contents of `.build/`.


### Ignore files

In each directory, in a file named `.noteignore` you can add one filename per line.
Then `note` will ignore those filenames for that directory.

For a git-like syntax for ignores, see github `bitranox/igittigitt`.  As of 2021-01, that was a more supported clone of `mherrmann/gitignore_parser`.


## Development

### todo

For ignore functionality, choose one of:

- `git`-style ignore specification
- a simpler, matching scheme that I implement in Python

Handle `.rst` files.

Implement user override for `css`, and `js`.

implement `note build show`.  
Detect appropriate browser and open `.build/index.html` in a new tab.