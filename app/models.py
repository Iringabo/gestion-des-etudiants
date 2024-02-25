from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid
from slugify import slugify


class UserProfilesManager(BaseUserManager):
    """Modele de gestion des profils utilisateur"""

    def _create_user(self, username, email, Nom, Prenom, password=None, **extra_fields):
        """Crée un utilisateur de base"""
        if not email:
            raise ValueError('Un utilisateur doit avoir un email')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, Nom=Nom, Prenom=Prenom, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, Nom, Prenom, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        return self._create_user(username, email, Nom, Prenom, password, **extra_fields)

    def create_superuser(self, username, email, Nom, Prenom, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')

        return self._create_user(username, email, Nom, Prenom, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    Nom = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    Prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    is_professeur = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfilesManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'Nom', 'Prenom']

    class Meta:
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"
        ordering = ["username"]
        db_table = "user_profile"
        permissions = [
            ("can_view_profile", "Can view profile"),
            ("can_edit_profile", "Can edit profile"),
        ]

    @property
    def nom(self):
        return str(self.Nom).upper()

    @property
    def prenom(self):
        return str(self.Prenom).capitalize()

    def __str__(self):
        return self.Nom + " / " + self.Prenom
class Etudiant(models.Model):
    CodeEtudiant = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    NomEtudiant = models.CharField(max_length=100)
    PrenomEtudiant = models.CharField(max_length=100)
    Matricule = models.CharField(max_length=255, unique=True)
    DateNaissance = models.DateTimeField(blank=False)



    def __str__(self):
        return self.NomEtudiant

    @property
    def nom(self):
        return str(self.NomEtudiant).upper()

    @property
    def prenom(self):
        return str(self.PrenomEtudiant).capitalize()


class Cours(models.Model):
    CodeCours = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    NomCours = models.CharField(max_length=255,unique=True)
    Volume = models.IntegerField(blank=False)



    def __str__(self):
        return self.NomCours


class Note(models.Model):
    CodeNote = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    createdOn = models.DateTimeField(auto_now=True)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    note = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['etudiant', 'cours'], name='unique_etudiant_cours')
        ]

    def save(self, *args, **kwargs):
        # Génère un slug aléatoire à partir de etudiant et du cours
        slug_str = "%s %s" % (self.etudiant.PrenomEtudiant, self.cours.NomCours)
        slug_str = slug_str.replace(' ', '-').lower()
        # Ajoute un suffixe numérique si le slug existe déjà
        count = 1
        slug = slug_str
        while Note.objects.filter(slug=slug).exists():
            slug = "%s-%d" % (slug_str, count)
            count += 1
        self.slug = slug
        # Enregistre le modèle avec le slug généré
        super(Note, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.etudiant.PrenomEtudiant} {self.etudiant.NomEtudiant} - {self.cours.NomCours}: {self.note}"
