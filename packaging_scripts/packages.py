import os
'''
Creates statrep.dtx and longfigure.dtx in subdirectories of current dir.
Files present:
    statrep.wrapper
    longfigure.wrapper
    longfigure.inc

statrep.wrapper is read and longfigure.inc is inserted to create statrep.dtx
longfigure.wrapper is read and longfigure.inc is inserted to create longfigure.dtx

'''

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

def write_dtx(name, lines):
    if not os.path.isdir(name):
        os.mkdir(name)
    fname = '%s/%s.dtx' % (name, name)
    with open(fname, 'wb') as f:
        f.writelines(lines)

def main():
    statrep = readfile('statrep.wrapper')
    longfigure = readfile('longfigure.wrapper')
    inc = readfile('longfigure.inc')

    write_dtx('statrep', insert(statrep, inc))
    write_dtx('longfigure', insert(longfigure, inc))



if __name__ == '__main__':
    main()