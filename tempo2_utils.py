# tempo2_utils.py

# Simple python functions to help gather results from tempo2

import numpy
import subprocess

def general2(parfile, timfile, params):
    """
    general2(parfile, timfile, params):

    Calls tempo2 with the general2 plugin, and reads the output.

    Inputs:
      parfile = string, name of parfile
      timfile = string, name of tim file
      params = list of general2 values to return

    Outputs:
      dict of numpy arrays for each requested param.

    Notes:
      Assumes each parameter results in a single text column in the general2
      output.  A few params (for example 'posPulsar') output multiple columns,
      using these will currently break things.

      Also currently assumes all outputs can be interpreted as floating
      point numbers.
    """

    id_str = 'ABCD'
    s_arg = id_str
    for p in params:
        s_arg += " {%s}" % p
    s_arg += "\\n"

    t2output = subprocess.check_output(["tempo2", "-nobs", "20000", 
        "-output", "general2", 
        "-f", parfile, timfile, 
        "-s", s_arg])

    goodlines = [x for x in t2output.split('\n') if x.startswith(id_str)]
    nline = len(goodlines)

    result = {}
    for p in params:
        # Note, assumes single output column per requested param
        # and that all values are numerical
        result[p] = numpy.zeros(nline)

    for i in range(nline):
        vals = goodlines[i].split()
        for ip in range(len(params)):
            result[params[ip]][i] = vals[ip+1]

    return result

def chi2(parfile,timfile):
    """
    Run tempo2, get chi2 (as reported by 'general' plugin)
    """

    id_str = 'ABCD'
    t2output = subprocess.check_output(["tempo2", "-nobs", "20000", "-output", "general",
        "-s", id_str+' ', "-f", parfile, timfile])

    goodlines = [x for x in t2output.split('\n') if x.startswith(id_str)]

    chi2 = 0.0
    for l in goodlines:
        vals = l.split()
        if vals[1]=='chisq' and vals[2]=='=':
            chi2 = float(vals[3])

    return chi2

def stats(parfile,timfile):
    """
    Run tempo2, get chi2, ndof, rms (as reported by 'general' plugin)
    """

    id_str = 'ABCD'
    t2output = subprocess.check_output(["tempo2", "-nobs", "20000", "-output", "general",
        "-s", id_str+' ', "-f", parfile, timfile])

    goodlines = [x for x in t2output.split('\n') if x.startswith(id_str)]

    chi2 = 0.0
    for l in goodlines:
        vals = l.split()
        if vals[1]=='chisq' and vals[2]=='=':
            chi2 = float(vals[3])

    return chi2





