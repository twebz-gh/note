#!/usr/bin/env python
"""
Catalog the note src dir tree to create index.html.
Along the way, convert input files to output files.
"""

import os
import shlex
import shutil
import subprocess
import sys
import time

from note_src import file


class Config():
    pass


class Dir():
    def __init__(self, parentdirs=[], name=''):
        self.dpath_src = cfg.dpath_src_root
        self.dpath_dst = cfg.dpath_build
        for pd in parentdirs:
            self.dpath_src = os.path.join(self.dpath_src, pd)
            self.dpath_dst = os.path.join(self.dpath_dst, pd)
        self.parentdirs = parentdirs
        self.name = name
        self.subdirs = []
        self.files = []
        os.makedirs(os.path.join(self.dpath_dst, self.name), exist_ok=True)
        self.populate()

    def ignore(self, fname):
        if fname[0] in '._':
            return True
        if fname.startswith('artifacts-develop-'):  #TODO rm this when proper ignore functionality is implemented
            return True
        #TODO handle other types of ignores

    def populate(self):
        dir_to_list = os.path.join(self.dpath_src, self.name)
        if cfg.verbose: print('Dir.populate()')
        if cfg.verbose: print('    os.listdir({}):  {}'.format(dir_to_list, sorted(os.listdir(dir_to_list))))
        for name in sorted(os.listdir(dir_to_list)):
            if self.ignore(name):
                continue
            parentdirs = self.parentdirs
            if self.name:
                parentdirs = self.parentdirs + [self.name]
            path = os.path.join(dir_to_list, name)
            if os.path.isdir(path):
                if cfg.verbose: print('Dir.populate()  isdir==True')
                if cfg.verbose: print('    parentdirs:  {}'.format(parentdirs))
                if cfg.verbose: print('    name:  {}'.format(name))
                self.subdirs.append(Dir(parentdirs, name))
            elif os.path.isfile(path):
                if cfg.verbose: print('Dir.populate()  isfile==True')
                if cfg.verbose: print('    parentdirs:  {}'.format(parentdirs))
                if cfg.verbose: print('    name:  {}'.format(name))
                self.files.append(file.File(parentdirs, name, cfg))

    def __str__(self):
        if self.name:
            text = len(self.parentdirs) * '    ' + self.name + '/'
        else:
            text = ''
        for d in self.subdirs:
            text += '\n' + str(d)
        for f in self.files:
            text += '\n' + str(f)
        return text

    def html(self):
        if self.name:
            text = len(self.parentdirs) * 4 * '&nbsp;' + self.name + '/'
        else:
            text = ''
        html = '<div class="directory">{}</div>'.format(text)
        for d in self.subdirs:
            html += '\n' + d.html()
        for f in self.files:
            html += '\n' + f.html()
        html += '\n'
        return html


def build():
    # As we walk the directory tree:
    # - create the output file for each input file
    # - assemble the content for the index file
    tree = Dir()
    index_file_content = tree.html()

    # Get the template file for index.html and do text replacements.
    html = open(cfg.fpath_template_index).read()
    html = html.replace('{{css}}', cfg.fpath_css_index)
    html = html.replace('{{content}}', index_file_content)

    # Write out index.html.
    open(cfg.fpath_index_html, 'w').write(html)


def get_timestamps():
    """Get the most recent timestamps for select files.

    These are used to determine whether an output file is out of date.
    """
    cfg.ts_index = max([os.path.getmtime(cfg.fpath_template_index),
                        os.path.getmtime(cfg.fpath_css_index)])
    cfg.ts_general = max([os.path.getmtime(cfg.fpath_css),
                          os.path.getmtime(cfg.fpath_js)])
    cfg.ts_markdown = max([cfg.ts_general, os.path.getmtime(cfg.fpath_template_markdown)])


def clean():
    """Delete build directory."""
    if cfg.dpath_build.endswith('.build'):
        cmd = shlex.split('rm -r {}'.format(cfg.dpath_build))
        if cfg.verbose:
            print(cmd)
        subprocess.call(cmd)
    else:
        sys.stderr.write("error:  dpath_build.endswith('.build') == False\n")


def find_dpath_note_root():
    """Find .noteignore closest to '/' in path of cwd return its absolute path."""
    dpath = '/'
    dnames = [] + os.getcwd().split('/')
    for dname in dnames:
        dpath = os.path.join(dpath, dname)
        if '.noteignore' in os.listdir(dpath):
            if cfg.verbose:
                print('dpath_note_root:  {}'.format(dpath))
            return dpath


def usage():
    usage  = 'usage: note build [-v]\n'
    usage += '       note clean'
    print(usage)


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ('build', 'make', 'clean'):
        usage()
        exit()

    cfg = Config()
    cfg.verbose = False
    if '-v' in sys.argv:
        cfg.verbose = True

    cfg.pandoc_major_version = None
    cfg.dpath_src_root = find_dpath_note_root()
    if not cfg.dpath_src_root:
        print('".noteignore" not found')
        exit()

    cfg.dpath_build = os.path.join(cfg.dpath_src_root, '.build')
    cfg.fpath_index_html = os.path.join(cfg.dpath_build, 'index.html')

    home = os.environ['HOME']
    dpath_static = os.path.join(home, '.local/config/note')
    cfg.fpath_css = os.path.join(dpath_static, 'css', 'default.css')
    cfg.fpath_css_index = os.path.join(dpath_static, 'css', 'index-default.css')
    cfg.fpath_js = os.path.join(dpath_static, 'js', 'default.js')
    cfg.fpath_template_markdown = os.path.join(dpath_static, 'template', 'markdown.html')
    cfg.fpath_template_index = os.path.join(dpath_static, 'template', 'index.html')
    #fpath_house_icon = os.path.join(dpath_static, 'img', '36451-gray-home-icon-vector.png')

    if sys.argv[1] in ('build', 'make'):
        get_timestamps()
        build()
    elif sys.argv[1] == 'clean':
        clean()
