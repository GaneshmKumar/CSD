# Codechef Solution Downloader (CSD)
Python script to download code chef solutions for a problem

# Modules used
* requests==2.17.3
* beautifulsoup4==4.6.0
* argparse==1.1

# Setup
1. Clone the repo using `git clone  https://github.com/GaneshmKumar/CSD.git`
2. `cd CSD`
3. `python setup.py install`

# Usage
`csd -pc maxsc -l c java pyth -sc ac wa -p 1`

* -pc - problem code
* -l - programming languages (c, java, pyth, etc..) #By default all languages will be downloaded
* -sc - status code (AC, WA, TLE) #By default AC will be downloaded
* p - total number of pages to download #By default all pages will be downloaded

The supported **compilers** and **status codes** are given below

## Compilers
* BF
* NEM
* TEXT
* JS
* LUA
* COB
* PIKE
* C#
* PYPY
* SCALA
* PERL
* ASM
* PYTH
* D
* HASK
* ADA
* GO
* RUBY
* BASH
* ICON
* ALL
* SCM_CHICKEN
* ST
* WSPC
* PERL6
* F#
* PHP
* PYTH 3.5
* CLPS
* CLOJ
* ERL
* PAS_GPC
* C++_6.3
* PAS_FPC
* TCL
* C++14
* CAML
* SWIFT
* PRLG
* RUST
* ICK
* SCM_QOBI
* C
* NODEJS
* C++_4.3.2
* FORT
* JAVA
* SCM_GUILE
* LISP_SBCL
* LISP_CLISP
* KOTLIN
* NICE

To know more about codechef supported compilers, visit https://www.codechef.com/wiki/list-compilers

## Status Codes
* AC - Correct Answer
* WA - Wrong Answer
* TLE - Time Limit Exceeded
* RTE - Run Time Error
* CTE - Compile Time Error
