#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import basename

docs = ['pisitools.py',
        'autotools.py',
        'libtools.py',
        'shelltools.py',
        'get.py',
        'kde.py']

standard = '\\layout Standard'
section = '\\layout Section'
subsection = '\\layout Subsection'
theend = '\\the_end'
lyxcode = '\\layout LyX-Code'

italic = '\\emph on'

lyx = '''#LyX 1.3 created this file. For more info see http://www.lyx.org/
\\lyxformat 221
\\textclass article
\\language turkish
\\inputencoding auto
\\fontscheme default
\\graphics default
\\paperfontsize default
\\papersize Default
\\paperpackage a4
\\use_geometry 0
\\use_amsmath 0
\\use_natbib 0
\\use_numerical_citations 0
\\paperorientation portrait
\\secnumdepth 3
\\tocdepth 3
\\paragraph_separation indent
\\defskip medskip
\\quotes_language english
\\quotes_times 2
\\papercolumns 1
\\papersides 1
\\paperpagestyle default

'''

def savelyx():
    global lyx
    lyx += theend + '\n'
    f = open(basename(__file__).split('.')[0] + '.lyx', 'w')
    f.write(lyx)
    f.close()

def makeSection(data):
    global lyx
    lyx += section + '\n' +\
           data.split('.')[0][0].upper() +\
           data.split('.')[0][1:] + '\n\n'

def makeSubSection(data):
    global lyx
    lyx += subsection + '\n' +\
           data[4:data.index('(')] + '\n\n'

def makeLyxCode(data):
    global lyx
    lyx += lyxcode + '\n' +\
           italic + '\n' +\
           data[data.index('('):data.index(')')+1] + '\n\n'

def makeStandard(data):
    global lyx
    lyx += standard + '\n' + data + '\n\n'

for doc in docs:
    makeSection(doc) 
    content = open(doc, 'r').readlines()
    for i in range(0, len(content)):
        if content[i].startswith('def '):
            makeSubSection(content[i])
            if content[i][content[i].index('(')+1][0] is not ')':
                makeLyxCode(content[i])
            else:
                makeLyxCode(content[i][:content[i].index('(') + 1] +\
                            'None' +\
                            content[i][content[i].index(')'):])
            if content[i+1].strip().startswith("'''"):
                makeStandard(content[i+1][content[i+1].index("'''") + 3 :\
                                          content[i+1].rindex("'''")])
    
savelyx() 
