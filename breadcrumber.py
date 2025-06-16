#!/bin/env python3

"""
Given an HTML file, replaces any instance of
  <BREADCRUMB></BREADCRUMB>
with a nev element based on the file path; something like

  <nav class='breadcrumb' aria-label='Breadcrumb'><ol><li><a href='../'>CS 418</a></li><li><a href='./'>Graphics explanatory texts</a></li><li><a aria-current='page'>Burley's Principled BRDF</a></li></ol></nav>

for a file named

  html/text/disney-brdf.html

This relies on the file being in an html/ tree with a parallel file in an md/ tree
"""

import sys
from os.path import *

if len(sys.argv) != 2:
  print(f"USAGE: {sys.argv[0]} html/path/to/buildfile.html", file=sys.stderr)
  quit(1)

src = open(sys.argv[1]).read()
if '<BREADCRUMB></BREADCRUMB>' not in src: quit(0)


raw = sys.argv[1]
dir = dirname(raw)
if basename(raw) == 'index.html': raw = dirname(raw)
if not raw.startswith('html/'):
  print(f"ERROR: path must be in html/ directory tree, not \"{raw}\"", file=sys.stderr)
  quit(0)

def titleof(path):
  title = basename(path).replace('.html','')
  md = 'md'+path[4:].replace('.html','.md')
  if isfile(md): f = md
  elif isdir(md) and exists(join(md,'index.md')): f = join(md,'index.md')
  else: return title

  cnt=0
  for line in open(f):
    if line.startswith('title: '):
      title = line[7:].strip()
      break
    cnt += 1
    if cnt > 5: break
  
  return title


remaining, final = split(raw)
crumbs = ["<nav class='breadcrumb' aria-label='Breadcrumb'><ol>"]
while len(remaining) >= 2:
  crumbs.insert(1, f"<li><a href='{relpath(remaining, dir)}/'>{titleof(remaining)}</a></li>")
  remaining, final = split(remaining)
crumbs.append(f"<li><a aria-current='page'>{titleof(raw)}</a></li>")
crumbs.append("</ol></nav>")



open(sys.argv[1],'w').write(src.replace('<BREADCRUMB></BREADCRUMB>', ''.join(crumbs)))
