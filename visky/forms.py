from django import forms


class AlcoForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput, label='Пошук')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].widget.attrs.update({'class': 'block  mt-2 placeholder-gray-400/70 dark:placeholder-gray-500 rounded-lg border border-gray-200' \
                                              'bg-white px-5 py-2.5 text-gray-700 focus:border-blue-400 focus:outline-none focus:ring focus:ring-blue-300' \
                                              'focus:ring-opacity-40 dark:border-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:focus:border-blue-300',
                                              'placeholder': 'Введіть тип алкоголю',
                                              'name': 'q',
                                              'id': 'search'}
                                              )
