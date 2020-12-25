#!/bin/bash

mkdir -p ~/.local/bin
mkdir -p ~/.local/config/note/css
mkdir -p ~/.local/config/note/img
mkdir -p ~/.local/config/note/js
mkdir -p ~/.local/config/note/template

cp note.py ~/.local/bin/note

cp css/default.css ~/.local/config/note/css/
cp img/36451-gray-home-icon-vector.svg ~/.local/config/note/img/
cp js/default.js ~/.local/config/note/js/

cp template/from-markdown.html ~/.local/config/note/template/
cp template/index.html ~/.local/config/note/template/

cp install.sh pseudocode.md Readme.md ~/.local/config/note/


