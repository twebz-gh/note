#!/usr/bin/env python
"""
Copied from ~/doc/sphinx/doc/replace-index-pages.py
Modify that to create the index.html, and along the way, convert
the files in doc/ to output files in build/.
"""

import os
import shlex
import shutil
import subprocess
import sys


def reformat_toc(toc_in):
    toc_in = '\n'.join(toc_in)
    toc_in = toc_in.replace('<ul>', '\n<ul>\n')
    toc_in = toc_in.replace('</ul>', '\n</ul>\n')
    toc_in = toc_in.split('\n')
    level = -2
    toc = []
    for line in toc_in:
        if '<ul>' in line:
            level += 1
            continue
        if '</ul>' in line:
            level -= 1
            continue
        if 'href' not in line:
            continue
        href_loc = line.find('href')
        quote1 = line.find('"')
        quote2 = line[quote1 + 1:].find('"') + quote1 + 1
        href = line[href_loc:quote2 + 1]
        line = line[quote2 + 2:]
        close = line.find('</a>')
        name = line[:close]
        name = level * 4 * '&nbsp;' + name
        item = '    <a {}>{}</a>\n'.format(href, name)
        toc.append(item)
    return toc


def extract_title(title_line):
    pos_gt = title_line.find('>')
    pos_lt = title_line.rfind('<')
    title = title_line[pos_gt + 1:pos_lt]
    return title


def get_html_and_toc(fpath_dst):
    main_div = []
    toc = []
    put_in_body = False
    put_in_toc = False
    title_line = ''
    for line in open(fpath_dst).readlines():
        if put_in_toc and line.startswith('</div>'):
            put_in_toc = False
        elif line.startswith('<div id="TOC">'):
            put_in_body = False
            put_in_toc = True
        elif line.startswith('<h1 '):
            put_in_body = True
            title_line = line
        elif line.startswith('</body>'):
            put_in_body = False

        if put_in_body:
            main_div.append(line)
        else:
            toc.append(line)
    toc = reformat_toc(toc)
    title = extract_title(title_line)
    toc[-1] = toc[-1].rstrip()  # remove the last '\n'
    toc = toc[1:]  # remove the title
    main_div[-1] = main_div[-1].rstrip()  # remove the last '\n'
    '''
    with open('main.html', 'w') as fp:
        for line in main_div:
            fp.write(line.strip() + '\n')
    with open('toc.html', 'w') as fp:
        for line in toc:
            fp.write(line.strip() + '\n')
    '''
    return main_div, toc, title


def customize_html(fpath_dst):
    fpath_home = os.path.join(dpath_build, 'index.html')
    fpath_css = os.path.join(dpath_static, 'css', 'default.css')
    fpath_js = os.path.join(dpath_static, 'js', 'default.js')
    #fpath_house_icon = os.path.join(dpath_static, 'img', '36451-gray-home-icon-vector.svg')
    fpath_house_icon = os.path.join(dpath_static, 'img', '36451-gray-home-icon-vector.png')

    main_div, toc, title = get_html_and_toc(fpath_dst)
    html = open(os.path.join(dpath_template, 'from-markdown.html')).read()
    #import pdb; pdb.set_trace()
    html = html.replace('{{main_div}}', ''.join(main_div))
    html = html.replace('{{toc}}', ''.join(toc))
    html = html.replace('{{css}}', fpath_css)
    html = html.replace('{{js}}', fpath_js)
    html = html.replace('{{home}}', fpath_home)
    html = html.replace('{{title}}', title)
    open(fpath_dst, 'w').write(html)


def handle_file_markdown(fpath_src, dpath_dst):
    fname_dst = os.path.basename(fpath_src).replace('.md', '.html')
    fpath_dst = os.path.join(dpath_dst, fname_dst)
    cmd = '''pandoc {}
             --from markdown
             --to html
             --standalone
             --toc
             --output={}
          '''.format(fpath_src, fpath_dst).strip()
    cmd = shlex.split(cmd)
    subprocess.call(cmd)
    customize_html(fpath_dst)
    return os.path.basename(fpath_dst)

def handle_file_pdf(fpath_src, dpath_dst):
    fname_dst = os.path.basename(fpath_src)
    fpath_dst = os.path.join(dpath_dst, fname_dst)
    shutil.copy(fpath_src, fpath_dst)
    return os.path.basename(fpath_dst)

def handle_file_ignore(fpath_src):
    """Handle a file that is ignored."""
    if verbose: print('ignore file:  {}'.format(fpath_src))


class File():
    def __init__(self, parentdirs, name):
        self.dpath_src = dpath_content
        self.dpath_dst = dpath_build
        for pd in parentdirs:
            self.dpath_src = os.path.join(self.dpath_src, pd)
            self.dpath_dst = os.path.join(self.dpath_dst, pd)
        self.parentdirs = parentdirs
        self.name_src = name
        self.fpath_src = os.path.join(self.dpath_src, self.name_src)
        if verbose: print('File.__init__()')
        if verbose: print('    self.dpath_src:  {}'.format(self.dpath_src))
        if verbose: print('    self.dpath_dst:  {}'.format(self.dpath_dst))
        if verbose: print('    self.parentdirs:  {}'.format(self.parentdirs))
        if verbose: print('    self.name_src:  {}'.format(self.name_src))
        if verbose: print('    self.fpath_src:  {}'.format(self.fpath_src))
        self.convert()

    def convert(self):
        if self.name_src.endswith('.md'):
            if verbose: print('File.convert()')
            if verbose: print('    self.fpath_src:  {}'.format(self.fpath_src))
            if verbose: print('    self.dpath_dst:  {}'.format(self.dpath_dst))
            self.name_dst = handle_file_markdown(self.fpath_src, self.dpath_dst)
        elif self.name_src.endswith('.pdf'):
            self.name_dst = handle_file_pdf(self.fpath_src, self.dpath_dst)
        else:
            if verbose: print('unhandled file type:  {}'.format(self.fpath_src))
            return
        self.fpath_dst = os.path.join(self.dpath_dst, self.name_dst)

    def __str__(self):
        return len(self.parentdirs) * '    ' + self.name_dst

    def html(self):
        if 'name_dst' not in self.__dict__:
            return ''
        indent = len(self.parentdirs) * 4 * '&nbsp;'
        text = self.name_dst
        if text.endswith('.html'):
            text = text[:-5]
        html = ('<div class="file"><span>{}</span><a href="{}">{}</a></div>'
                ''.format(indent, self.fpath_dst, text))
        return html


class Dir():
    def __init__(self, parentdirs=[], name=''):
        self.dpath_src = dpath_content
        self.dpath_dst = dpath_build
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
        #TODO handle other types of ignores

    def populate(self):
        dir_to_list = os.path.join(self.dpath_src, self.name)
        if verbose: print('Dir.populate()')
        if verbose: print('    os.listdir({}):  {}'.format(dir_to_list, sorted(os.listdir(dir_to_list))))
        for name in sorted(os.listdir(dir_to_list)):
            if self.ignore(name):
                continue
            parentdirs = self.parentdirs
            if self.name:
                parentdirs = self.parentdirs + [self.name]
            path = os.path.join(dir_to_list, name)
            if os.path.isdir(path):
                if verbose: print('Dir.populate()  isdir==True')
                if verbose: print('    parentdirs:  {}'.format(parentdirs))
                if verbose: print('    name:  {}'.format(name))
                self.subdirs.append(Dir(parentdirs, name))
            elif os.path.isfile(path):
                if verbose: print('Dir.populate()  isfile==True')
                if verbose: print('    parentdirs:  {}'.format(parentdirs))
                if verbose: print('    name:  {}'.format(name))
                self.files.append(File(parentdirs, name))

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
    # read the directory tree for dirs and files we care about
    tree = Dir()
    # generate html for the relevant dirs and files
    content = tree.html()

    # read the template file and add in the generated table-of-contents
    fpath_index_template = os.path.join(dpath_template, 'index.html')
    html = open(fpath_index_template).read()
    html = html.replace('{{content}}', content)

    # write out the result
    fpath_out = os.path.join(dpath_build, 'index.html')
    open(fpath_out, 'w').write(html)


def usage():
    usage  = 'usage: note build [-v]\n'
    usage += '       note clean'
    print(usage)


def find_dpath_content():
    """Find .../note-foo/content and return its path."""
    dname = 'note-'

    # If `note` was called from note-foo root directory.
    cwd = os.getcwd()
    if os.path.basename(cwd).startswith(dname) and 'content' in os.listdir(cwd):
        return os.path.join(cwd, 'content')

    # If `note` was called from deeper within note-foo.
    names = cwd.split('/')
    while True:
        if len(names) < 2:
            break
        if names[-2].startswith(dname) and names[-1] == 'content':
            return os.path.join('/', '/'.join(names))
        names[:] = names[:-1]


def clean():
    txt = 'rm -r {}/*'.format(dpath_build)
    if not dpath_build.endswith('build') and 'note-' not in dpath_build:
        raise Exception('abort call:  {}'.format(txt))
    for name in os.listdir(dpath_build):
        # Use this way of constructing the path-to-be-deleted to ensure that
        # only items under a 'build/' are deleted.
        path = os.path.join(os.path.dirname(dpath_build), 'build', name)
        cmd = shlex.split('rm -r {}'.format(path))
        subprocess.call(cmd)


if __name__ == '__main__':
    verbose = False
    if len(sys.argv) < 2 or sys.argv[1] not in ('build', 'make', 'clean'):
        usage()
        exit()
    if '-v' in sys.argv:
        verbose = True

    dpath_content = find_dpath_content()
    if not dpath_content:
        print('content directory for "note" not found')
        exit()
    dpath_build = os.path.join(os.path.dirname(dpath_content), 'build')
    home = os.environ['HOME']
    dpath_static = os.path.join(home, '.local/config/note')
    dpath_template = os.path.join(dpath_static, 'template')

    if sys.argv[1] in ('build', 'make'):
        build()
    elif sys.argv[1] == 'clean':
        clean()
