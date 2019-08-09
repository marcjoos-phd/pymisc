#!/usr/bin/env python
#===============================================================================
#> \file getenv.py
## \brief
## \b Get (modified) bash environment in Python
## \author
## Marc Joos <marc.joos@gmail.com>
## \copyright
## Copyrights 2019, Marc Joos
## This file is distributed under the CeCILL-A & GNU/GPL licenses, see
## <http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html> and
## <http://www.gnu.org/licenses/>
#<
#===============================================================================

import os
import subprocess as sp

def get_env(out, encoding='utf-8'):
    """Retrieve an environment from a bash standard output, assuming that a 'printenv' command was executed.

    Usage:
      new_env = get_env(out [, encoding])
    With:
      out:       string containing a standard output including a bash 'printenv' call
      encoding:  encoding of the processed standard output (default: 'utf-8')
    Returns:
      new_env:   dict of the retrieved environment (similar to os.environ)
    """
    lout = str(out[0], encoding).split('\n')

    new_env = {}
    nlines = len(lout)
    iloc = 0
    for i in range(nlines):
        iloc = max(i, iloc)
        line = lout[iloc]
        if len(line.split('=')) <= 1:
            pass
        elif "{" in line and not "}" in line:
            k = line.split("=")[0]
            v = "=".join(line.split("=")[1:])
            new_env[k] = v
            while not line[-1] == "}":
                iloc += 1
                line = lout[iloc]
                new_env[k] = new_env[k] + "\n" + line
        else:
            k = line.split("=")[0]
            v = "=".join(line.split("=")[1:])
            new_env[k] = v
    return new_env

def launch(cmd_, env=os.environ, get_env=False):
    """Launch a bash command.          
    It is both possible to specify an environment and to retrieve the environment from the bash subprocess.

    Usage:
      err, out = launch(cmd [, env, get_env])          

    With:
      cmd:     a bash command        
      env:     (optional) a dict of the environment to load (default: os.environ)                   
      get_env: (optional) if 'True', retrieve the environment from the bash subprocess                  
    Returns:
      err:     error code
      out:     standard output and standard error from the bash command(s)                        
    """
    if get_env: cmd_ += " && printenv"
    load = sp.Popen(cmd_, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, env=env)
    out  = load.communicate()
    err  = load.returncode
    return(err, out)
