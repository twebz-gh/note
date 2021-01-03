# Note

## Install

For '.rpm' based linux:  `yum install pandoc`.

For '.deb' based linux:  `apt install pandoc`.

Get the source and install:
```bash
$ cd
$ mkdir -p app/note
$ cd note
$ git clone <url>
$ cd note
$ ./install.sh
```


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
        lasagne.md
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

Imagine a bookmark folder that you put in the bookmark bar near the top of your browser.
Let `note build` update one link in that folder to link to the current doc tree.

Implement `git`-style `ignore` specification.

Handle `.rst` files.

Implement user override for `css`, and `js`.

Only build files that are out of date.

