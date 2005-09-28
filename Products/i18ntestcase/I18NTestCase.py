#
# i18ntestcase
#

from Testing import ZopeTestCase
from glob import glob
import os, re, sys
import os.path
import htmlentitydefs

try:
    import win32api
    WIN32 = True
except ImportError:
    WIN32 = False

def getFileFromPath(path):
    if WIN32:
        file = path.split('\\')[-1]
    else:
        file = path.split('/')[-1]
    return file

def getLanguageFromPath(path):
    file = getFileFromPath(path)
    # strip of .po
    file = file[:-3]
    lang = file.split('-')[1:]
    return '-'.join(lang)

def getProductFromPath(path):
    file = getFileFromPath(path)
    # strip of .pot
    file = '-'.join(file.split('.')[:1])
    prod = '-'.join(file.split('-')[:1])
    return prod

def getPotFiles(path='..'):
    path = os.path.normpath(path)
    productPath = os.path.join(path, '..')
    i18nPath = os.path.join(productPath, 'i18n')
    if not os.path.isdir(i18nPath):
        i18nPath = productPath
    potFiles= glob(os.path.join(i18nPath, '*.pot'))

    potFiles = [pot for pot in potFiles if not (pot.endswith('manual.pot') or pot.endswith('generated.pot') or pot.endswith('combinedchart.pot'))]

    if not potFiles:
        raise IOError('No pot files found in %s!' % i18nPath)
    return potFiles

def getPoFiles(path='..', product=''):
    path = os.path.normpath(path)
    productPath = os.path.join(path, '..')
    i18nPath = os.path.join(productPath, 'i18n')
    if not os.path.isdir(i18nPath):
        i18nPath = productPath
    poFiles=glob(os.path.join(i18nPath, '%s-*.po' % product))
    return poFiles

class I18NTestCase(ZopeTestCase.ZopeTestCase):
    '''Base test case for i18n testing'''

    # html entities as they appear in templates
    ENTITIES = ['&'+ent+';' for ent in htmlentitydefs.entitydefs if ent not in ['hellip','mdash','trade']]

    # these are taken from PTS, used for format testing
    NAME_RE = r"[a-zA-Z][a-zA-Z0-9_]*"
    _interp_regex = re.compile(r'(?<!\$)(\$(?:%(n)s|{%(n)s}))' %({'n': NAME_RE}))

    def isEntity(self, msgstr):
        # no html-entities in msgstr
        found = [entity for entity in self.ENTITIES if entity in msgstr]
        if len(found) > 0:
            return (True, 'Error: html-entities %s' % found)
        return (False, None)

    def isMalformedMessageVariable(self, msgstr):
        # every ${foo} is properly closed
        if not (msgstr.count('${') - msgstr.count('}') == 0):
            return (True, 'Error: Misformed message variable ${foo}')
        return (False, None)

    def getMessageVariables(self, msg, default):
        # get message variables from the default
        if default:
            default_vars = self._interp_regex.findall(default)
        else:
            default_vars = self._interp_regex.findall(msg)
        return default_vars

    def isMessageVariablesMissing(self, msgstr, default_vars=[]):
        # all ${foo}'s from the default should be present in the translation
        default_vars = [unicode(var) for var in default_vars]
        msg_vars = [unicode(var) for var in self._interp_regex.findall(msgstr)]
        missing = [var for var in default_vars if var not in msg_vars]
        if missing:
            return (True, 'Warning: Missing message attributes %s' % missing)
        return (False, None)



