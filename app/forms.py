from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Etudiant, UserProfile


class EtudiantForm(forms.Form):
    etudiant = forms.ModelChoiceField(queryset=Etudiant.objects.all())


class SignupForm(UserCreationForm):
    is_professeur = forms.BooleanField(required=False)

    class Meta:
        model = UserProfile
        fields = UserCreationForm.Meta.fields + \
            ('username', 'Nom', 'Prenom', 'email', 'is_professeur')

    def try_save(self, request):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email
