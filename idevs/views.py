from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import ConductorForm

from textwrap import dedent
import csv
from io import StringIO

conds="""\
condid,description,R_ohms,X_ohms,B_mhos,sn_amps,se_amps
1,795 ACSR 26/7 (Drake),0.129605,0.758057,5.63327E-06,1001,1451
2,2 - 954 ACSR 54/7 (Cardinal),0.0547515,0.5737005,7.34216E-06,2226,3246
3,1 - 1590 ACSR 54/19 (Falcon),0.06625725,0.76215675,5.5879E-06,1551,2347\
"""
f = StringIO(conds)
reader = csv.DictReader(f)
CONDS = [cond for cond in reader]

for cond in CONDS:
    float_fields = ['R_ohms', 'X_ohms', 'B_mhos', 'sn_amps', 'se_amps']
    for key in float_fields:
        cond[key] = float(cond[key])
    cond['condid'] = int(cond['condid'])

def get_cond(condid):
    ret = CONDS[0]
    condid = condid
    for cond in CONDS:
        if cond['condid'] == condid:
            ret = cond
    return ret

def cond_pu(cond, kv, length):
    """
    Get per unit data for conductor
    Args:
        cond: conductor dictionary
        kv: line voltage
        lenght: length of line in miles
    Returns: conductor dictionary
    """
    kv = float(kv)
    amps_to_mva = 3.0**0.5 * kv / 1000.0
    Zbase = kv**2/100.0
    Ybase = 1.0/Zbase
    cond['sn_mva'] = round(cond['sn_amps'] * amps_to_mva)
    cond['se_mva'] = round(cond['se_amps'] * amps_to_mva)
    cond['Rpu'] = cond['R_ohms'] * length / Zbase
    cond['Xpu'] = cond['X_ohms'] * length / Zbase
    cond['Bpu'] = cond['B_mhos'] * length / Ybase
    return cond

def index(request):
    context = {}
    template = loader.get_template('idevs/index.html')
    return HttpResponse(template.render(context, request))

def branch(request):
    if request.method == 'POST':
        form = ConductorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            kv = data['kv']
            ll = data['line_length']
            cond = get_cond(data['condid'])
            cond = cond_pu(cond, kv, ll)
            cond['length'] = ll
            cond['to_bus'] = data['to_bus']
            cond['from_bus'] = data['from_bus']
            cond['ckt'] = data['ckt']
            cond['owner'] = 'OWNER'

            #flash('IDEV Created') # right now there is nowhere in HTML to receive the flash
            idev = dedent("""\
                    @! Branch is: %(description)s %(length)s mi
                    BAT_BRANCH_DATA,%(to_bus)s,%(from_bus)s,'%(ckt)s',,,%(owner)s,,,,%(Rpu)7f,%(Xpu)7f,%(Bpu)7f,%(sn_mva)d,%(se_mva)d,%(se_mva)d,,,,,%(length)s,,,,,;\
                    """) % cond
        else:
            idev = 'ERROR'
    else:
        form = ConductorForm()
        idev = 'CREATE BRANCH ...'

    context = {'form': form, 'idev': idev}
    template = loader.get_template('idevs/branch.html')
    return HttpResponse(template.render(context, request))
