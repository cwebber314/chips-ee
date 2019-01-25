from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import BranchIdevForm, BusIdevForm, TransformerIdevForm

#import pdb

from textwrap import dedent
import csv
from io import StringIO

conds="""\
condid,description,R_ohms,X_ohms,B_mhos,R0_ohms,X0_ohms,B0_mhos,sn_amps,se_amps
1,795 ACSR 26/7 (Drake),0.13064184,0.78423192,5.49254E-06,0.42887088,1.78213752,3.32388E-06,1001,1451
2,2 - 954 KCM ACSR (Cardinal),0.057132,0.55584675,7.78996E-06,0.35588475,1.55327625,3.75047E-06,2226,3246
3,1590 KCM ACSR (Falcon),0.0690345,0.74390625,8.25676425,0.366597,1.742526,4.57651125,1551,2347
"""
f = StringIO(conds)
reader = csv.DictReader(f)
CONDS = [cond for cond in reader]

for cond in CONDS:
    float_fields = ['R_ohms', 'X_ohms', 'B_mhos', 'R0_ohms', 'X0_ohms', 'B0_mhos', 'sn_amps', 'se_amps']
    for key in float_fields:
        cond[key] = float(cond[key])
    cond['condid'] = int(cond['condid'])

def get_cond(condid):
    ret = None
    condid = int(condid)
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

    cond['R0pu'] = cond['R0_ohms'] * length / Zbase
    cond['X0pu'] = cond['X0_ohms'] * length / Zbase
    cond['B0pu'] = cond['B0_mhos'] * length / Ybase
    return cond

def index(request):
    context = {}
    template = loader.get_template('power/index.html')
    return HttpResponse(template.render(context, request))

def branch(request):
    if request.method == 'POST':
        form = BranchIdevForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            kv = data['kv']
            ll = data['line_length']
            #pdb.set_trace()
            cond = get_cond(data['condid'])
            cond = cond_pu(cond, kv, ll)
            cond['length'] = ll
            cond['to_bus'] = data['to_bus']
            cond['from_bus'] = data['from_bus']
            cond['ckt'] = data['ckt']
            cond['owner'] = data['owner']
            cond['kv'] = kv

            #flash('IDEV Created') # right now there is nowhere in HTML to receive the flash
            idev = dedent("""\
                @! Branch is: %(description)s %(length)s mi at %(kv)s kV
                BAT_BRANCH_DATA,%(from_bus)s,%(to_bus)s,'%(ckt)s',,,%(owner)s,,,,%(Rpu)7f,%(Xpu)7f,%(Bpu)7f,%(sn_mva)d,%(se_mva)d,%(se_mva)d,,,,,%(length)s,,,,,;
                BAT_SEQ_BRANCH_DATA_3,%(from_bus)s,%(to_bus)s,'%(ckt)s',,%(R0pu)7f,%(X0pu)7f,%(B0pu)7f,,,,,,;
                """) % cond
        else:
            idev = 'ERROR'
    else:
        form = BranchIdevForm()
        idev = 'CREATE BRANCH ...'

    context = {'form': form, 'idev': idev}
    template = loader.get_template('power/branch.html')
    return HttpResponse(template.render(context, request))

def bus(request):
    if request.method == 'POST':
        form = BusIdevForm(request.POST)
        if form.is_valid():
            idev = dedent("""\
                    @! TODO: Fix this.  Add the Nominal KV
                    BAT_BUS_DATA_3,%(busnum)d,%(ide)s,%(area)s,%(zone)s,%(owner)s,0.0, 1.0,0.0, 1.1, 0.9, 1.1, 0.9,'%(busname)s'\
                    """)
            data = form.cleaned_data
            idev = idev % data
        else:
            idev = 'ERROR'
    else: # Get
        form = BusIdevForm()
        idev = 'CREATE BUS ...'

    context = {'form': form, 'idev': idev}
    template = loader.get_template('power/bus.html')
    return HttpResponse(template.render(context, request))

def transformer2w(request):
    if request.method == 'POST':
        form = TransformerIdevForm(request.POST)
        if form.is_valid():
            idev = dedent("""\
                BAT_TWO_WINDING_DATA_3, %(from_bus)d, %(to_bus)d, '%(ckt)s', 1,
                %(from_bus)d, %(owner)d, 0, 0, 0, 33, 0, %(from_bus)d, 0, 1, 0, 1, 2, 1,
                %(R).5f, %(X).5f, 100.0, .99, %(from_bus_kv).1f, 0.0, 1.0,
                %(to_bus_kv).1f, %(norm_mva)d, %(emer_mva)d, %(emer_mva)s, 1.0, 1.0, 1.0, 1.0, 0.0,
                0.0, 1.1, 0.9, 1.1, 0.9, 0.0, 0.0, 0.0, '%(name)s'
                """)
            data = form.cleaned_data
            data['from_bus_kv'] = float(data['from_bus_kv'])
            data['to_bus_kv'] = float(data['to_bus_kv'])
            idev = idev % data
        else:
            idev = "ERROR"
    else:
        form = TransformerIdevForm()
        idev = 'BAT_TWO_WINDING_DATA_3 ...'

    context = {'form': form, 'idev': idev}
    template = loader.get_template('power/transformer2w.html')
    return HttpResponse(template.render(context, request))

def tline_map(request):
    template = loader.get_template('power/tline_map.html')
    context = {}
    return HttpResponse(template.render(context, request))
