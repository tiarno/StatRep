import filecmp
import os
import shutil
import shlex
import subprocess
import time
import zipfile

ROOT = os.getcwd()
SUPPLEMENT = os.path.join(ROOT, 'supplement')
CONTENT = os.path.join(ROOT, 'content')
BUILD = os.path.join(ROOT, 'build')
BENCH = os.path.join(ROOT, 'benchmark')
SASCMD = None
DEVNULL = open(os.devnull, 'wb')


def chmods(dirname):
    for root, dnames, files in os.walk(os.path.join(ROOT, dirname)):
        for dname in dnames:
            fullname = os.path.join(root, dname)
            os.chmod(fullname, 0755)

        for fname in files:
            fullname = os.path.join(root, fname)
            os.chmod(fullname, 0644)

def unixlines(dirname):
    skip_exts = ['.pdf', '.png', '.jpg']
    for root, dnames, files in os.walk(os.path.join(ROOT, dirname)):
        for fname in files:
            fullname = os.path.join(root, fname)
            stem, ext = os.path.splitext(fname)
            if ext and ext in skip_exts:
                continue

            with open(fullname) as f:
                lines = f.readlines()

            newlines = [line.replace('\r\n', '\n') for line in lines]
            with open(fullname, 'w') as f:
                f.writelines(newlines)

def zipdir(fullpath):
    '''
    Splits fullpath into its last directory name (package)
    and the parent (dirpath). Creates a zip file named package.zip in the parent
    which contains the files in fullpath.
    '''
    package = os.path.basename(fullpath)
    dirpath = os.path.dirname(fullpath)
    z = zipfile.ZipFile(os.path.join(dirpath, '%s.zip' % package), 'w')
    for root, _, fnames in os.walk(os.path.join(dirpath, package)):
        for fname in fnames:
            fullname = os.path.join(root, fname)
            relroot = os.path.relpath(root, dirpath)
            arcname = os.path.join(relroot, fname)
            if os.path.isfile(fullname):
                z.write(fullname, arcname)
    z.close()

def pdf(fname, cwd):
    cmd = str('pdflatex %s' % fname)
    p = subprocess.Popen(shlex.split(cmd), stdout=DEVNULL,
                        stderr=subprocess.STDOUT,
                        cwd=cwd)
    p.wait()

def idx(fname, cwd):
    fname, ext = os.path.splitext(fname)
    if ext == '.dtx':
        option = ' -s gind.ist '
    else:
        option =''
    cmd = str('makeindex %s %s' % (option, fname))
    p = subprocess.Popen(shlex.split(cmd), stdout=DEVNULL,
                         stderr=subprocess.STDOUT, cwd=cwd)
    p.wait()

class Tester(object):
    def __init__(self):
        if not SASCMD:
            self.sascmd = raw_input('Enter your batch SAS command: ')
        else:
            self.sascmd = SASCMD
        self.cwd = os.path.join(BUILD, 'test')
        cmd = str('%s statrep_tagset.sas' % self.sascmd)
        p = subprocess.Popen(shlex.split(cmd), cwd=self.cwd)
        p.wait()
        self.tests = 0
        self.passed = 0
        names = ['statrep', 'longfigure']
        for name in names:
            src = os.path.join(BUILD, 'work', name, '%s.sty' % name)
            tgt = os.path.join(BENCH, '%s.sty' % name)
            shutil.copy(src, tgt)

    def test(self):
        names = ['example', 'quickstart', 'testcases']
        for name in names:
            pdf('%s.tex' % name, self.cwd)
        for name in names:
            cmd = str('%s %s_SR.sas' % (self.sascmd, name))
            p = subprocess.Popen(shlex.split(cmd), cwd=self.cwd)
            p.wait()
            pdf('%s.tex' % name, self.cwd)
            pdf('%s.tex' % name, self.cwd)

    def diff(self):
        names = ['testcases', 'example', 'quickstart']
        for name in names:
            cmd = str('gs -sDEVICE=jpeg -dNOPAUSE -dBATCH -dSAFER ')
            cmd += str('-sOutputFile=%s%%08d.jpg %s.pdf' % (name[0], name))

            p = subprocess.Popen(shlex.split(cmd), stdout=DEVNULL,
                                 stderr=subprocess.STDOUT,
                                 cwd=BENCH, )
            p.wait()
            p = subprocess.Popen(shlex.split(cmd), stdout=DEVNULL,
                                 stderr=subprocess.STDOUT,
                                 cwd=os.path.join(BUILD, 'test'))
            p.wait()

        files = [x for x in os.listdir(BENCH) if x.endswith('jpg')]
        for fname in files:
            self.tests += 1
            if not filecmp.cmp(os.path.join(BENCH, fname),
                               os.path.join(BUILD, 'test', fname)):
                print 'Diff for %s' % fname
            else:
                self.passed += 1
        print 'Total tests: %d. Passed: %d. Failed: %d' % (self.tests, self.passed, (self.tests - self.passed))


class Packager(object):
    def __init__(self):
        if os.path.isdir(BUILD):
            shutil.rmtree(BUILD)
            time.sleep(2)

        self.ctan = os.path.join(BUILD, 'ctan')
        self.work = os.path.join(BUILD, 'work')
        self.test = os.path.join(BUILD, 'test')
        self.sas = os.path.join(BUILD, 'sas')
        for fname in [x for x in os.listdir(BENCH) if x.endswith('.jpg')]:
            os.unlink(os.path.join(BENCH, fname))


        unixlines('content');
        unixlines('supplement')
        chmods('content');
        chmods('supplement')
        self.makedirs()
        self.getcontent()

    def makedirs(self):
        for dname in [self.ctan, self.sas]:
            os.makedirs(os.path.join(dname, 'statrep', 'doc'))
            os.makedirs(os.path.join(dname, 'statrep', 'sas'))
            os.makedirs(os.path.join(dname, 'longfigure'))

        os.makedirs(self.test)
        os.makedirs(os.path.join(self.work, 'statrep'))
        os.makedirs(os.path.join(self.work, 'longfigure'))

    def getcontent(self):
        self.content = dict()
        with open(os.path.join(CONTENT, 'statrep.wrapper')) as f:
            self.content['statrep'] = f.readlines()
        with open(os.path.join(CONTENT, 'longfigure.wrapper')) as f:
            self.content['longfigure'] = f.readlines()
        with open(os.path.join(CONTENT, 'longfigure.inc')) as f:
            self.content['common'] = f.readlines()

    def write_dtx(self):
        def insert_common(wrapper):
            newlines = list()
            for line in self.content[wrapper]:
                newlines.append(line)
                if line.strip() == '%    \\label{longfigure}':
                    newlines.extend(self.content['common'])
            return newlines

        for name in ['statrep', 'longfigure']:
            cwd = os.path.join(self.work, name)
            with open(os.path.join(cwd, '%s.dtx' % name), 'wb') as f:
                f.writelines(insert_common(name))

    def run_dtx(self):
        for name in ['statrep', 'longfigure']:
            cwd = os.path.join(self.work, name)
            pdf('%s.dtx' % name, cwd);idx('%s.dtx' % name, cwd);
            pdf('%s.dtx' % name, cwd);pdf('%s.dtx' % name, cwd)

    def makemanual(self):
        cwd = os.path.join(self.work, 'statrep')
        shutil.copytree(os.path.join(SUPPLEMENT, 'images'), os.path.join(cwd, 'images'))
        for fname in ['example.tex','statrepmanual.tex']:
            shutil.copy(os.path.join(SUPPLEMENT, fname),
                        os.path.join(cwd, fname))

            if fname == 'statrepmanual.tex':
                pdf(fname, cwd);idx(fname, cwd);
                pdf(fname, cwd);pdf(fname, cwd)

    def setup_tests(self):
        for fname in ['testcases.tex', 'example.tex', 'quickstart.tex',
                      'statrep_macros.sas', 'statrep_tagset.sas']:
            shutil.copy(os.path.join(SUPPLEMENT, fname),
                        os.path.join(self.test, fname))

        for name in ['statrep', 'longfigure']:
            shutil.copy(os.path.join(self.work, name, '%s.sty' % name),
                        os.path.join(self.test, '%s.sty' % name))

    def setup_delivery(self, package_name):
        if package_name == 'ctan':
            cwd = self.ctan
        elif package_name == 'sas':
            cwd = self.sas

        for name in ['statrep', 'longfigure']:
            shutil.copy(os.path.join(SUPPLEMENT, 'LICENSE'),
                        os.path.join(cwd, name, 'LICENSE'))

            shutil.copy(os.path.join(self.work, name, 'README.'),
                        os.path.join(cwd, name, 'README'))
            for fname in ['%s.dtx' % name, '%s.ins' % name]:
                shutil.copy(os.path.join(self.work, name, fname),
                            os.path.join(cwd, name, fname))

            if name == 'longfigure':
                shutil.copy(os.path.join(self.work, name, '%s.pdf' % name),
                            os.path.join(cwd, name, '%s.pdf' % name))

            elif name == 'statrep':
                tcwd = os.path.join(cwd, 'statrep', 'sas')
                for fname in ['statrep_macros.sas', 'statrep_tagset.sas']:
                    shutil.copy(os.path.join(SUPPLEMENT, fname),
                                os.path.join(tcwd, fname))

                tcwd = os.path.join(cwd, 'statrep', 'doc')
                shutil.copytree(os.path.join(SUPPLEMENT, 'images'), os.path.join(tcwd, 'images'))
                shutil.copy(os.path.join(SUPPLEMENT, 'quickstart.tex'),
                            os.path.join(tcwd, 'quickstart.tex'))

                for fname in ['statrep.pdf', 'statrepmanual.pdf', 'statrepmanual.tex']:
                    shutil.copy(os.path.join(self.work, name, fname),
                                os.path.join(tcwd, fname))

                if package_name == 'sas':
                    for fname in ['longfigure.sty', 'statrep.sty']:
                        shutil.copy(os.path.join(self.work, name, fname),
                                    os.path.join(cwd, name, fname))


if __name__ == '__main__':
    p = Packager()
    p.write_dtx()
    p.run_dtx()
    p.makemanual()
    print '-'*30
    p.setup_tests()
    p.setup_delivery('ctan')
    p.setup_delivery('sas')

    t = Tester()
    t.test()
    t.diff()
    zipdir(os.path.join(p.ctan, 'statrep'))
    zipdir(os.path.join(p.sas, 'statrep'))

    if t.tests == t.passed:
        for fname in [x for x in os.listdir(BENCH) if x.endswith('.jpg')]:
            os.unlink(os.path.join(BENCH, fname))
        print 'Ready for upload. See %s' % BUILD





