#!/bin/bash

mkdir -p ~/.local/bin/note_src
mkdir -p ~/.local/config/note/css
mkdir -p ~/.local/config/note/img
mkdir -p ~/.local/config/note/js
mkdir -p ~/.local/config/note/template

rm -rf ~/.local/bin/note_src/*
cp note.py ~/.local/bin/note
cp -r note_src ~/.local/bin/

cp css/default.css ~/.local/config/note/css/
cp css/index-default.css ~/.local/config/note/css/
cp img/36451-gray-home-icon-vector.svg ~/.local/config/note/img/
cp js/default.js ~/.local/config/note/js/

cp template/markdown.html ~/.local/config/note/template/
cp template/index.html ~/.local/config/note/template/

cp README.md ~/.local/config/note/


