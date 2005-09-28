"""
Unit tests for translation files

References:
http://i18n.kde.org/translation-howto/check-gui.html#check-msgfmt

The testNoDuplicateMsgId() method was taken and slightly modified from
http://svn.nuxeo.org/trac/pub/file/CPSI18n/trunk/tests/translations.py
"""

import os, os.path, re
import i18ntestcase
from popen2 import popen4

MSGID_REGEXP = re.compile('msgid "(.*?)".*?msgstr "', re.DOTALL)

class PotTestCase(I18NTestCase.I18NTestCase):
    pot = None
    path = os.curdir
    
    def testNoDuplicateMsgId(self):
        """Check that there are no duplicate msgids in the pot files"""
        pot = '%s.pot' % self.pot
        path = self.path
        file = open(os.path.join(path, pot), 'r')
        file_content = file.read()
        file.close()

        # Check for duplicate msgids
        matches = re.finditer(MSGID_REGEXP, file_content)
        msgids = []
        for match in matches:
            msgid = match.group(0)
            if msgid in msgids:
                assert 0, "Duplicate msgids were found in file \"%s\":\n\n%s" \
                       % (pot, msgid)
            else:
                msgids.append(msgid)

