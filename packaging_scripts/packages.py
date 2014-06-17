import os
import shutil
import shlex
import subprocess
import time

'''
Creates statrep.dtx and longfigure.dtx in appropriate subdirectories.
Files present:
    statrep.wrapper
    longfigure.wrapper
    longfigure.inc

statrep.wrapper is read and longfigure.inc is inserted to create statrep.dtx
longfigure.wrapper is read and longfigure.inc is inserted to create longfigure.dtx

'''
ROOT = os.path.normpath(os.path.join(os.getcwd(), '..'))

EXTRAS = os.path.join(ROOT, 'extras')

#
CTAN = os.path.join(ROOT, 'ctan')
TESTING = os.path.join(ROOT, 'testing')


def run_pdf(name):
    def pdf():
        cmd = str('pdflatex %s.dtx' % name)
        p = subprocess.Popen(shlex.split(cmd), cwd=cwd)
        p.wait()
    def idx():
        cmd = str('makeindex -s gind.ist %s' % name)
        p = subprocess.Popen(shlex.split(cmd), cwd=cwd)
        p.wait()

    cwd = os.path.join(TESTING, name)
    pdf();pdf()
    idx();pdf()

def start_clean():
    for d in [CTAN, TESTING]:
        if os.path.isdir(d):
            for f in os.listdir(d):
                fname = os.path.join(d, f)
                if os.path.isfile(fname):
                    os.unlink(fname)
            shutil.rmtree(d)
            time.sleep(2)
        os.mkdir(d)


def readfile(name):
    with open(name) as f:
        lines = f.readlines()
    return lines

def insert(wrapper, content):
    newlines = list()
    for line in wrapper:
        newlines.append(line)
        if line.strip() == '%    \\label{longfigure}':
            newlines.extend(content)

    return newlines

def write_dtx(package, lines):
    dname = os.path.join(TESTING, package)
    fname = os.path.join(TESTING, package, '%s.dtx' % package)
    if not os.path.isdir(dname):
        os.mkdir(dname)

    with open(fname, 'wb') as f:
        f.writelines(lines)

def copyfiles(package):
    tgtdir = os.path.join(CTAN, package)
    if not os.path.isdir(tgtdir):
        os.mkdir(tgtdir)

    src =  os.path.join(TESTING, package, 'README.')
    tgt = os.path.join(tgtdir, 'README')
    shutil.copy(src, tgt)

    for ext in ['dtx', 'ins', 'pdf']:
        src = os.path.join(TESTING, package, '%s.%s' % (package, ext))
        tgt = os.path.join(tgtdir, '%s.%s' % (package, ext))
        shutil.copy(src, tgt)

    if package == 'statrep':
        for dname in [CTAN, TESTING]:
            tgtdir = os.path.join(dname, package)
            for name in os.listdir(EXTRAS):
                src = os.path.join(EXTRAS, name)
                tgt = os.path.join(tgtdir, name)
                shutil.copy(src, tgt)

def main():
    start_clean()
    statrep = readfile('statrep.wrapper')
    longfigure = readfile('longfigure.wrapper')
    inc = readfile('longfigure.inc')

    write_dtx('statrep', insert(statrep, inc))
    write_dtx('longfigure', insert(longfigure, inc))

    run_pdf('statrep')
    run_pdf('longfigure')

    copyfiles('statrep')
    copyfiles('longfigure')


if __name__ == '__main__':
    main()