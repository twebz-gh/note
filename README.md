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

Create a directory with a name that start with `note-`.  Inside that, make a directory named `content`.
```bash
$ mkdir note-hobby/content
```
Under `content/`, create a file tree of your notes, like this example:
```
note-hobby/
    build/        # web pages created by `note` from your files
    content/      # files you write
        rc-plane/
            .note-ignore
            hobby-zone-champ.md
            hobby-zone-sport-cub-s.md
            umx-radian.md
            delta-ray.md
        food/
            lasagne.md
            brats-n-kraut.md
            brown-the-butter.md
```

### Build

Navigate to anywhere inside `note-hobby/`, then do:
```
$ note build
```
Then `note` will convert your files in `content/` to an html tree in `build/`.
Navigate your browser to `file://...build/index.html`.


### Clean

Navigate to anywhere inside `note-hobby/`, then do:
```
$ note clean
```
Then `note` will delete the contents of `build/`.


### Ignore files

In each directory, in a file named `.note-ignore` you can add one filename per line.
Then `note` will ignore those filenames for that directory.


## Development

### todo

Imagine a bookmark folder that you put in the bookmark bar near the top of your browser.
Let `note build` update one link in that folder to link to the current doc tree.

Implement `git`-style `ignore` specification.

Handle `.rst` files.

Implement user override for `css`, and `js`.

