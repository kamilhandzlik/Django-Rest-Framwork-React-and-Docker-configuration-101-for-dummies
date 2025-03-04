# Django REST Framework, React and Docker Configuration 101 for Dummies

## Wstęp

Cześć!  
Poniżej znajdziesz krótki poradnik, jak założyć projekt w Django i skonfigurować w nim Django REST Framework oraz React.

**WAŻNE!!!**  
Ten setup działa na dzień 4.03.2025. W zależności od tego, kiedy korzystasz z tego poradnika, niektóre jego elementy mogą być przestarzałe.

---

## I. Django

### 1. Zakładanie wirtualnego środowiska

Aby rozpocząć, zainstaluj `virtualenv` i utwórz nowe wirtualne środowisko:

1. Zainstaluj `virtualenv`:
    ```bash
    pip install virtualenv
    ```
2. Utwórz nowe wirtualne środowisko:
    ```bash
    python -m virtualenv nazwa_środowiska  # najlepiej 'env' lub 'venv'
    ```
3. Aktywuj wirtualne środowisko:
   - **Dla Windowsa (nie zapomnij o kropce na początku!):**
     ```bash
     . venv/Scripts/activate
     ```
   - **Dla Linuxa:**
     ```bash
     source venv/bin/activate
     ```

### 2. Wykonanie odpowiednich instalacji

Można skorzystać z pliku `requirements.txt`, umieszczonego w tym repozytorium. Jeśli go nie masz, stwórz go w tym samym katalogu co pliki `venv` i `README` i dodaj poniższe linie:

django python-decouple djangorestframework django-extensions


Alternatywnie, zainstaluj rozszerzenia ręcznie za pomocą poleceń w terminalu:

```bash
pip install django
pip install python-decouple
pip install django-extensions
pip install djangorestframework
3. Konfiguracja pliku settings.py
W pliku settings.py dodaj następujące aplikacje do listy INSTALLED_APPS:

INSTALLED_APPS = [
    ...,
    "django_extensions",
    "rest_framework",
]
Dalej, dodaj import w settings.py:

from decouple import config
4. Zabezpieczanie SECRET_KEY
W tym samym katalogu, co plik manage.py, stwórz plik .env.

Zapisz w nim:

SECRET_KEY="wpisz swój klucz"
W settings.py zamień SECRET_KEY na poniższą linię:

SECRET_KEY = config("SECRET_KEY")
Następnie, przejdź do terminala i wygeneruj nowy SECRET_KEY:

python manage.py generate_secret_key
Wygenerowany klucz dodaj do pliku .env:

SECRET_KEY=nowy-wygenerowany-klucz
5. Konfiguracja Django REST Framework (DRF) w settings.py (opcjonalne, ale zalecane)
Na końcu pliku settings.py dodaj poniższą konfigurację:


REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",  # Wyświetlanie UI z Django REST Framework
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}
6. Tworzenie aplikacji dla API
W terminalu wpisz:

python manage.py startapp api
Następnie, dodaj aplikację do INSTALLED_APPS w settings.py:


INSTALLED_APPS = [
    ...,
    "django_extensions",
    "rest_framework",
    "api.apps.ApiConfig",  #  Jest to w ścieżka do klasy która powstaje w pliku apps nowo powstałej aplikacji, która zawsze będzie się nazywać NazwaAplikacjiConfig 
]

7. Tworzenie pierwszego modelu
Załóżmy, że tworzysz API do zarządzania książkami. W pliku models.py aplikacji api dodaj model:


from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    publish_date = models.DateField(blank=True)

    def __str__(self):
        return f"{self.title or 'Brak tytułu'} - {self.author or 'Brak autora'} - {self.publish_date or 'Brak daty'}"
Nie zapomnij zrobić migracji:


python manage.py makemigrations api
python manage.py migrate
Zachowanie blank=True w DateField
Jeśli napiszesz:

publish_date = models.DateField(blank=True)
Django pozwoli na zapis pustego pola w formularzu (ModelForm), ale baza danych wciąż wymaga wartości, więc próbując zapisać model bez daty, dostaniesz błąd IntegrityError.

Aby pole było opcjonalne w bazie danych, musisz dodać:

publish_date = models.DateField(blank=True, null=True)
blank=True – Django nie będzie wymagać wartości w formularzach.
null=True – W bazie danych pole może być NULL.
8. Tworzenie serializera
W pliku serializers.py w aplikacji api dodaj serializer:

from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
Możesz także ręcznie wypisać pola, które chcesz, aby były serializowane:

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publish_date']
9. Tworzenie widoków API
W pliku views.py w aplikacji api dodaj widoki dla API:


from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
10. Dodanie URL-i dla API
W pliku api/urls.py stwórz ścieżki:

from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDestroyView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
]
Teraz podłącz je do głównego pliku urls.py projektu:

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Dodanie ścieżek API
]
11. Uruchomienie serwera i testowanie API
Uruchom serwer Django:

python manage.py runserver
Teraz możesz sprawdzić swoje API w przeglądarce lub za pomocą narzędzi takich jak curl lub Postman:

Lista książek: http://127.0.0.1:8000/api/books/
Detale książki: http://127.0.0.1:8000/api/books/1/

