import os
import shlex
import shutil
import subprocess
import sys
import time


cfg = None


"""On ubuntu 20.04:

$ pandoc --version
pandoc 2.5
Compiled with pandoc-types 1.17.5.4, texmath 0.11.2.2, skylighting 0.7.7
Default user data directory: /home/tony/.pandoc
Copyright (C) 2006-2018 John MacFarlane
Web:  http://pandoc.org
This is free software; see the source for copying conditions.
There is no warranty, not even for merchantability or fitness
for a particular purpose.

$ cat /etc/os-release
NAME="Ubuntu"
VERSION="20.04.2 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.2 LTS"
VERSION_ID="20.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=focal
UBUNTU_CODENAME=focal

$ python
Python 3.8.5
"""
def get_pandoc_major_version():
    cmd = 'pandoc --version'
    cmd = shlex.split(cmd)
    if sys.version_info < (3, 0):
        stdout = subprocess.check_output(cmd)
    elif sys.version_info >= (3, 7):
        stdout = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, text=True).stdout
    else:
        stdout = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True).stdout
    stdout = stdout.split('\n')[0]
    stdout = stdout.split(' ')[1]
    stdout = stdout.split('.')[0]
    major_version = int(stdout)
    return major_version


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
    #import pdb; pdb.set_trace()
    if toc:
        toc[-1] = toc[-1].rstrip()  # remove the last '\n'
        toc = toc[1:]  # remove the title
    if main_div:
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


def replace_html_template_elements(fpath_dst):
    main_div, toc, title = get_html_and_toc(fpath_dst)
    html = open(cfg.fpath_template_markdown).read()
    html = html.replace('{{main_div}}', ''.join(main_div))
    html = html.replace('{{toc}}', ''.join(toc))
    html = html.replace('{{css}}', cfg.fpath_css)
    html = html.replace('{{js}}', cfg.fpath_js)
    html = html.replace('{{index_page}}', cfg.fpath_index_html)
    html = html.replace('{{title}}', title)
    open(fpath_dst, 'w').write(html)


def handle_file_markdown(fpath_src, dpath_dst):
    fname_dst = os.path.basename(fpath_src).replace('.md', '.html')
    fpath_dst = os.path.join(dpath_dst, fname_dst)
    if os.path.exists(fpath_dst):
        mtime = os.path.getmtime(fpath_dst)
        if mtime > cfg.ts_markdown and mtime > os.path.getmtime(fpath_src):
            # The output file is already up to date.
            return fname_dst
    if not cfg.pandoc_major_version:
        cfg.pandoc_major_version = get_pandoc_major_version()
    cmd = '''pandoc {}
             --from markdown+superscript
             --to html
             --standalone
             --toc
             --output={}
          '''.format(fpath_src, fpath_dst).strip()
    if cfg.pandoc_major_version and cfg.pandoc_major_version >= 2:
        cmd += ' --quiet'
    cmd = shlex.split(cmd)
    subprocess.call(cmd)
    replace_html_template_elements(fpath_dst)
    return fname_dst

def handle_file_pdf(fpath_src, dpath_dst):
    fname_dst = os.path.basename(fpath_src)
    fpath_dst = os.path.join(dpath_dst, fname_dst)
    if os.path.exists(fpath_dst) and os.path.getmtime(fpath_dst) > cfg.ts_general:
        # The output file is already up to date.
        return fname_dst
    shutil.copy(fpath_src, fpath_dst)
    return fname_dst

def handle_file_ignore(fpath_src):
    """Handle a file that is ignored."""
    if cfg.verbose: print('ignore file:  {}'.format(fpath_src))


class File():
    def __init__(self, parentdirs, name, cfg_in):
        global cfg
        cfg = cfg_in
        self.dpath_src = cfg.dpath_src_root
        self.dpath_dst = cfg.dpath_build
        for pd in parentdirs:
            self.dpath_src = os.path.join(self.dpath_src, pd)
            self.dpath_dst = os.path.join(self.dpath_dst, pd)
        self.parentdirs = parentdirs
        self.name_src = name
        self.fpath_src = os.path.join(self.dpath_src, self.name_src)
        if cfg.verbose: print('File.__init__()')
        if cfg.verbose: print('    self.dpath_src:  {}'.format(self.dpath_src))
        if cfg.verbose: print('    self.dpath_dst:  {}'.format(self.dpath_dst))
        if cfg.verbose: print('    self.parentdirs:  {}'.format(self.parentdirs))
        if cfg.verbose: print('    self.name_src:  {}'.format(self.name_src))
        if cfg.verbose: print('    self.fpath_src:  {}'.format(self.fpath_src))
        self.convert()

    def convert(self):
        if self.name_src.endswith('.md'):
            if cfg.verbose: print('File.convert()')
            if cfg.verbose: print('    self.fpath_src:  {}'.format(self.fpath_src))
            if cfg.verbose: print('    self.dpath_dst:  {}'.format(self.dpath_dst))
            self.name_dst = handle_file_markdown(self.fpath_src, self.dpath_dst)
        elif self.name_src.endswith('.pdf'):
            self.name_dst = handle_file_pdf(self.fpath_src, self.dpath_dst)
        else:
            if cfg.verbose: print('unhandled file type:  {}'.format(self.fpath_src))
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
