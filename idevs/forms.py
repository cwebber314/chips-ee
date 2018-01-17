from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder
from crispy_forms.bootstrap import StrictButton, FormActions

KV_CHOICES = (
    ('138', 138.0),
    ('161', 161.0),
    ('230', 230.0),
    ('345', 345.0),
    )
COND_CHOICES = (
    (1, '795 ACSR 26/7 (Drake)'),
    (2, '2 - 954 ACSR 54/7 (Cardinal)'),
    (3, '1 - 1590 ACSR 54/7 (Falcon)'),
    )

class ConductorForm(forms.Form):
    kv = forms.ChoiceField(choices=KV_CHOICES)
    condid = forms.ChoiceField(choices=COND_CHOICES)
    line_length = forms.FloatField(label="Line Length (mi)", initial=1.0)
    to_bus = forms.CharField(label="To Bus", initial="TOBUS")
    from_bus = forms.CharField(label="From Bus", initial="FROMBUS")
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
            FormActions(
                Submit('create_idev', 'Create IDEV')
                )
            )

        super(ConductorForm, self).__init__(*args, **kwargs)
