# coding: utf-8
#===============================================================================
#> \file template.py
## \brief
## \b File template in Python
## \author
## Marc Joos <marc.joos@gmail.com>
## \copyright
## Copyrights 2019, Marc Joos
## This file is distributed under the CeCILL-A & GNU/GPL licenses, see
## <http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html> and
## <http://www.gnu.org/licenses/>
#<
#===============================================================================

import sys
if sys.version_info[0] <= 2:
    from commands import getstatusoutput as cmd
else:
    from subprocess import getstatusoutput as cmd

templt = "template.tex"
report = "doc.tex"

st, out = cmd('cp ' + templt + " " + report)
template = open(report, 'rt').read()
data = {"subsection1": "My awesome first subsection",
        "item2": "an awesome item",
        "fig1": "/path/with/image.png",
        "elt2": "3",
        "date1": "17-12-2018",
        "date2": "18-12-2018",
        "version": "1.0"}
with open(report, "wt") as output:
    output.write(template %data)
   
st, out = cmd('pdflatex ' + report)
