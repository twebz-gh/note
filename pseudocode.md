# pseudocode


`$ note build`
```
content root = search for content root
mkdir build
tree = create a tree of dirs and files under 'content'
for sub-directory in content root
    ignore_globals, ignore-local = load ignore files
    for src in `content/'  # ignore hidden files
        if src is in files-to-ignore
            continue
        calc corresponding dst in `build/`
        if dst is newer than src
            continue
        if src name ends with `.md`
            handle_markdown_file(src, dst)
        if src name ends with `.foo`
            handle_foo(src, dst)
```


handle_markdown_file:
```
convert src to dst
get body and toc from dst
add link to dst to index.html
load md-to-html template, and replace
    css
    js
    toc
    body
```


print tree - the file toc:
```py
class Node():
    indent_sz = 4

    def __init__(self, rfpath, is_root=False):
        # rfpath is relative to dpath_build_root
        self.is_root = is_root
        self.indent_num_spaces = Node.indent_sz * (len(os.path.split(rfpath)) - 1)
        self.name = os.path.basename(rfpath)
        self.link = os.path.join(dpath_build_root, rfpath)
        self.html = self.indent_len * &nbsp; + '<a href="{}">{}</a>'.format(self.link, self.name)
        self.dirs = []
        self.files = []

    def print(self):
        if not self.is_root:
            print(self.html)
        for d in sorted(self.dirs):
            d.print()
        for f in sorted(self.files):
            f.print()
```

