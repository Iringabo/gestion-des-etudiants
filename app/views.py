import statistics
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import  ListView, CreateView,UpdateView, DeleteView
from app.models import Note, Etudiant, Cours
from django.http import HttpResponse
from django.views import View
import pandas as pd
from django.db.models import Q

@method_decorator(login_required, name='dispatch') 
class acceuil(ListView):
    model = Note
    context_object_name = 'form'
    template_name = 'index.html'
    paginate_by = 10
    login_url = '/accounts/login'
    redirect_field_name = 'account_login'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            return queryset.filter(
                Q(note__icontains=q) |
                Q(etudiant__NomEtudiant__icontains=q) |
                Q(etudiant__PrenomEtudiant__icontains=q) |
                Q(cours__NomCours__icontains=q) |
                Q(etudiant__Matricule__icontains=q)
            )
        return queryset
def EcarType(request):
    etudiants = Etudiant.objects.all()
    selected_etudiant = None
    if request.method == 'POST':
        selected_etudiant = Etudiant.objects.get(
            CodeEtudiant=request.POST['etudiant'])
        notes = selected_etudiant.note_set.all().values_list('note', flat=True)
        if len(notes) > 1:
            selected_etudiant.ecart_type = statistics.stdev(notes)
        else:
            selected_etudiant.ecart_type = 0
    return render(request, 'detail.html', {'etudiants': etudiants, 'selected_etudiant': selected_etudiant})

@method_decorator(login_required, name='dispatch')
class ExporterExcelView(View):
    def get(self, request, *args, **kwargs):
        # Récupérer les données de la base de données
        queryset = Note.objects.select_related('etudiant', 'cours').all()

        # Convertir le queryset en une liste de dictionnaires
        data = queryset.values('CodeNote', 'etudiant__NomEtudiant', 'etudiant__PrenomEtudiant',
                               'cours__NomCours', 'cours__Volume', 'note', 'createdOn')

        # Convertir la liste de dictionnaires en un DataFrame pandas
        df = pd.DataFrame.from_records(data)

        # Rendre les objets datetime indépendants du fuseau horaire
        df['createdOn'] = df['createdOn'].dt.tz_convert(None)

        # Créer une réponse HTTP avec un type de contenu Excel
        response = HttpResponse(content_type='application/vnd.ms-excel')

        # Créer un nom de fichier
        response['Content-Disposition'] = 'attachment; filename=Note2.xlsx'

        # Écrire le DataFrame dans la réponse HTTP
        df.to_excel(response, index=False)

        return response

@method_decorator(login_required, name='dispatch')
class EtudiantForm(CreateView):
    model = Etudiant
    fields = "__all__"
    context_object_name = 'form'
    template_name = 'etudiant.html'
    success_url = reverse_lazy('app:acceuil')
    login_url = '/accounts/login'
    redirect_field_name = 'account_login'

@method_decorator(login_required, name='dispatch')
class CoursForm(CreateView):
    model = Cours
    fields = "__all__"
    context_object_name = 'form'
    template_name = 'cours.html'
    success_url = reverse_lazy('app:acceuil')
    login_url = '/accounts/login'
    redirect_field_name = 'account_login'


class NoteForm(CreateView):
    model = Note
    fields = "__all__"
    context_object_name = 'form'
    template_name = 'note.html'
    success_url = reverse_lazy('app:acceuil')
    login_url = '/accounts/login'
    redirect_field_name = 'account_login'

class NoteUP(UpdateView):
    model = Note
    fields = "__all__"  # Specify the fields you want to display/edit in the form
    template_name = 'noteu.html'  # Specify the template to render the form
    success_url = "/"

class NoteD(DeleteView):
    model = Note
    template_name = 'noted.html'
    context_object_name = "note"
    success_url = "/"


