from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder
from crispy_forms.bootstrap import StrictButton, FormActions

KV_CHOICES = (
    ('69', 69.0),
    ('115', 115.0),
    ('138', 138.0),
    ('161', 161.0),
    ('230', 230.0),
    ('345', 345.0),
    ('500', 500.0),
    ('765', 765.0),
    )
COND_CHOICES = (
    (1, '1 - 1590 ACSR 54/7 (Falcon)'),
    (2, '2 - 954 ACSR 54/7 (Cardinal)'),
    (3, '795 ACSR 26/7 (Drake)'),
    (4, '3 - 954 ACSR 54/7 (Cardinal) [17 ft SPECIAL]'),
    )

class BusIdevForm(forms.Form):
    busnum = forms.IntegerField(label="Bus", initial=99999)
    busname = forms.CharField(label="Bus Name", initial="NSUB")
    buskv = forms.FloatField(label="Bus kV", initial=345.0)
    ide = forms.ChoiceField(choices=[(1, '1:Non-Generator Bus'), (2, 'Generator Bus'), (3, 'Swing Bus')])
    area = forms.IntegerField(label="Area", initial=2)
    zone = forms.IntegerField(label="Zone", initial=3)
    owner = forms.IntegerField(label="Owner", initial=520)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        helper = self.helper
        helper.form_method = 'POST'

        helper.form_class = 'form-horizontal'
        helper.label_class = 'col-sm-3'
        helper.field_class = 'col-sm-9'
        helper.layout = Layout(
            'busnum',
            'busname',
            'buskv',
            'ide',
            'area',
            'zone',
            'owner',
            FormActions(
                Submit('create_idev', 'Create IDEV')
                )
            )

        super(BusIdevForm, self).__init__(*args, **kwargs)

class TransformerIdevForm(forms.Form):
    from_bus = forms.IntegerField(label="From Bus", initial=100)
    from_bus_kv = forms.ChoiceField(choices=KV_CHOICES)
    to_bus = forms.IntegerField(label="To Bus", initial=101)
    to_bus_kv = forms.ChoiceField(choices=KV_CHOICES)
    ckt = forms.CharField(label="Ckt Id", initial="1")
    name = forms.CharField(label="Name", initial="NEW XFMR")
    owner = forms.IntegerField(label="Owner", initial=520)
    R = forms.FloatField(label="R", initial=0.001)
    X = forms.FloatField(label="X", initial=0.04)
    norm_mva = forms.FloatField(label="Normal Rating (MVA)", initial=600)
    emer_mva = forms.FloatField(label="Emergency Rating (MVA)", initial=660)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        helper = self.helper
        helper.form_method = 'POST'

        helper.form_class = 'form-horizontal'
        helper.label_class = 'col-sm-3'
        helper.field_class = 'col-sm-9'
        helper.layout = Layout(
            'from_bus',
            'from_bus_kv',
            'to_bus',
            'to_bus_kv',
            'ckt',
            'name',
            'owner',
            'R',
            'X',
            'norm_mva',
            'emer_mva',
            FormActions(
                Submit('create_idev', 'Create IDEV')
                )
            )
        super(TransformerIdevForm, self).__init__(*args, **kwargs)


class BranchIdevForm(forms.Form):
    kv = forms.ChoiceField(choices=KV_CHOICES)
    condid = forms.ChoiceField(choices=COND_CHOICES)
    line_length = forms.FloatField(label="Line Length (mi)", initial=1.0)
    from_bus = forms.IntegerField(label="From Bus", initial=100)
    to_bus = forms.IntegerField(label="To Bus", initial=101)
    owner = forms.IntegerField(label="Owner", initial=520)
    ckt = forms.CharField(label="Ckt Id", initial="1")

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        helper = self.helper
        helper.form_method = 'POST'

        helper.form_class = 'form-horizontal'
        helper.label_class = 'col-sm-3'
        helper.field_class = 'col-sm-9'
        helper.layout = Layout(
            'kv',
            'condid',
            'line_length',
            'to_bus',
            'from_bus',
            'ckt',
            'owner',
            FormActions(
                Submit('create_idev', 'Create IDEV')
                )
            )
        super(BranchIdevForm, self).__init__(*args, **kwargs)
