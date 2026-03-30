from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'short_description',
            'ingredients',
            'instructions',
            'prep_time',
            'cook_time',
            'servings',
            'difficulty',
            'category',
            'cuisine_type',
            'image',
            'is_published',
            'is_featured',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Inserisci il titolo della ricetta',
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Breve descrizione della ricetta',
            }),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Inserisci un ingrediente per riga oppure una lista ordinata',
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Descrivi il procedimento passo-passo',
            }),
            'prep_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'cook_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
            }),
            'difficulty': forms.Select(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'cuisine_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Es. Italiana, Giapponese, Messicana',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 3:
            raise forms.ValidationError('Il titolo deve contenere almeno 3 caratteri.')
        return title

    def clean_prep_time(self):
        prep_time = self.cleaned_data['prep_time']
        if prep_time < 1:
            raise forms.ValidationError('Il tempo di preparazione deve essere maggiore di 0.')
        return prep_time