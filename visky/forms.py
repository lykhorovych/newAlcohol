from django import forms


class AlcoForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput, label='Пошук')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].widget.attrs.update({'class': 'input input-bordered input-accent w-full max-w-xs',
                                              'placeholder': 'Введіть тип алкоголю',
                                              'name': 'q',
                                              'id': 'search'}
                                              )
