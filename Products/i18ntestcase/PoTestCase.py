import os, re
import i18ntestcase
from I18NTestCase import getFileFromPath, getLanguageFromPath

from popen2 import popen4
from gettext import GNUTranslations
from Products.PlacelessTranslationService import msgfmt
from i18ndude import catalog

class PotPoTestCase(I18NTestCase.I18NTestCase):
    pot = None
    po = None
    path = os.curdir

    def testMsgExists(self):
        """Check that the pot file has the same msgids as the po file"""
        po = self.po
        poName = os.path.split(po)[-1]
        pot = self.pot
        poEnglish = '%s-en.po' % pot[:-4]
        path = os.path.normpath(self.path)
        if not po.endswith(poEnglish):
            os.environ['LC_ALL']='C'
            o,i = popen4('msgcmp --directory=%s %s %s' % (path, poName, pot))
            del os.environ['LC_ALL']
            i.close()
            output = o.read()
            o.close()
            if output:
                output = output.split('\n')
                if len(output) > 10:
                    output = output[:10]
                    output.append('... <more errors>')
                output = '\n'.join(output)
                self.fail("Comparing %s with %s using msgcmp resulted in:\n%s" % (
                              pot, poName, output))

class PoTestCase(I18NTestCase.I18NTestCase):
    po = None
    product = None
    pot_cat = None

    def testPoFile(self):
        po = self.po
        product = self.product
        pot_cat = self.pot_cat
        poName = getFileFromPath(po)
        file = open(po, 'r')
        try:
            lines = file.readlines()
        except IOError, msg:
            self.fail('Can\'t read po file %s:\n%s' % (poName,msg))
        file.close()
        try:
            mo = msgfmt.Msgfmt(lines)
        except msgfmt.PoSyntaxError, msg:
            self.fail('PoSyntaxError: Invalid po data syntax in file %s:\n%s' % (poName, msg))
        except SyntaxError, msg:
            self.fail('SyntaxError: Invalid po data syntax in file %s (Can\'t parse file with eval():\n%s' % (poName, msg))
        except Exception, msg:
            self.fail('Unknown error while parsing the po file %s:\n%s' % (poName, msg))
        try:
            tro = GNUTranslations(mo.getAsFile())
        except UnicodeDecodeError, msg:
            self.fail('UnicodeDecodeError in file %s:\n%s' % (poName, msg))
        except msgfmt.PoSyntaxError, msg:
            self.fail('PoSyntaxError: Invalid po data syntax in file %s:\n%s' % (poName, msg))

        domain = tro._info.get('domain', None)
        self.failUnless(domain, 'Po file %s has no domain!' % po)

        language = tro._info.get('language-code', None)
        self.failUnless(language, 'Po file %s has no language!' % po)

        fileLang = getLanguageFromPath(po)
        language = language.replace('_', '-')
        self.failUnless(fileLang == language,
            'The file %s has the wrong name or wrong language code. expected: %s, got: %s' % (poName, language, fileLang))

        msgcatalog = [(msg, tro._catalog.get(msg)) for msg in tro._catalog if msg]

        for msg, msgstr in msgcatalog:
            # every ${foo} is properly closed
            if '${' in msgstr:
                status, error = self.isMalformedMessageVariable(msgstr)
                self.failIf(status, '%s in file %s:\n %s' % (error, poName, msg))
            # no html-entities in msgstr
            if '&' in msgstr and ';' in msgstr:
                status, error = self.isEntity(msgstr)
                self.failIf(status, '%s in file %s:\n %s' % (error, poName, msg))
            # all ${foo}'s from the default should be present in the translation
            default = pot_cat.getDefault(msg)
            default_vars = self.getMessageVariables(msg, default)
            if not default_vars is []:
                status, error = self.isMessageVariablesMissing(msgstr, default_vars=default_vars)
                self.failIf(status, '%s in file %s: %s' % (error, poName, msg))

