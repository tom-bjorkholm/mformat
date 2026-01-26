#! /bin/zsh
#
# Copyright (c) 2026 Tom Björkholm
# MIT License
#
git update-index --no-assume-unchanged example/result/*.docx
git update-index --no-assume-unchanged example/result/*.odt
mv .gitignore .gitignore.bak
cat .gitignore.bak | sed 'sXexample/result/..docxX# example/result/*.docxX' | \
sed 'sXexample/result/..odtX# example/result/*.odtX' > .gitignore
