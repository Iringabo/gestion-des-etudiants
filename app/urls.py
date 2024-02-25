from django.urls import path
from app.views import (acceuil, ExporterExcelView,
                       EcarType, EtudiantForm, CoursForm, NoteForm,NoteUP,NoteD)

app_name = "app"

urlpatterns = [
    path('', acceuil.as_view(), name='acceuil'),
    path('exporter_excel/', ExporterExcelView.as_view(), name='exporter_excel'),
    path('ecartype/', EcarType, name='detail'),
    path('etudiant/', EtudiantForm.as_view(), name='etudiant'),
    path('cours/', CoursForm.as_view(), name='cours'),
    path('note/', NoteForm.as_view(), name='note'),
    path('note/<str:slug>/update/', NoteUP.as_view(), name='noteu'),
    path('note/<str:slug>/delete/', NoteD.as_view(), name='noted'),

]