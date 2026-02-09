#! /bin/zsh
#
# Copyright (c) 2026 Tom Björkholm
# MIT License
#
git update-index --assume-unchanged example/result/*.docx
git update-index --assume-unchanged example/result/*.odt
mv .gitignore .gitignore.bak
cat .gitignore.bak | sed 'sX# example/result/..docxXexample/result/*.docxX' | \
sed  'sX# example/result/..odtXexample/result/*.odtX' > .gitignore
