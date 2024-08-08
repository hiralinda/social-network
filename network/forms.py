from django import forms

BACKGROUND_CHOICES = [
    ('linear-gradient(to right, #bdc3c7, #2c3e50);', 'Grade Gray'),
    ('linear-gradient(to right, #2980b9, #6dd5fa, #ffffff)', 'Cool Sky'),
    ('linear-gradient(to right, #1f4037, #99f2c8);', 'Harvey'),
    ('linear-gradient(to right, #ffefba, #ffffff);', 'Margo'),
    ('linear-gradient(to right, #ef3b36, #ffffff);', 'Compare Now'),
    ('linear-gradient(to right, #12c2e9, #c471ed, #f64f59);', 'JShine'),
    ('linear-gradient(to right, #f0f2f0, #000c40);', 'What Lies Beyond'),
]
class BackgroundForm(forms.Form):
    background_choice = forms.ChoiceField(choices=BACKGROUND_CHOICES, widget=forms.RadioSelect)
