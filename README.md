# Django REST Framework, React i Docker - Konfiguracja 101 dla Początkujących

## Wstęp

Cześć!
Ten poradnik pomoże Ci skonfigurować Django REST Framework oraz React w jednym projekcie.

**Uwaga:** Ten setup działa na dzień **4.03.2025**. W przyszłości niektóre elementy mogą wymagać aktualizacji.

---

## I. Konfiguracja Django i Django REST Framework

### 1. Tworzenie wirtualnego środowiska

Aby rozpocząć, zainstaluj `virtualenv` i utwórz nowe wirtualne środowisko:

```bash
pip install virtualenv
python -m virtualenv venv  # Nazwa środowiska najlepiej 'venv'
```

Aktywacja środowiska:
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```

### 2. Instalacja wymaganych pakietów

Możesz skorzystać z pliku `requirements.txt`. Jeśli go nie masz, utwórz i dodaj:

```
django
python-decouple
djangorestframework
django-extensions
```

Aby zainstalować zależności:
```bash
pip install -r requirements.txt
```

Alternatywnie, instalacja ręczna:
```bash
pip install django python-decouple djangorestframework django-extensions
```

### 3. Konfiguracja `settings.py`
Dodaj wymagane aplikacje do `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...,
    "django_extensions",
    "rest_framework",
]
```

Dodaj import w `settings.py`:
```python
from decouple import config
```

### 4. Zabezpieczenie `SECRET_KEY`

1. W katalogu projektu utwórz plik `.env` i dodaj:
    ```
    SECRET_KEY="twoj-tajny-klucz"
    ```
2. W `settings.py` zamień klucz na:
    ```python
    SECRET_KEY = config("SECRET_KEY")
    ```
3. Aby wygenerować nowy klucz:
    ```bash
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ```
    lub użyj tej komendy wykorzystującej django extensions pamiętaj tylko żeby usunąć wszystkie znaki '#' z klucza
    ```bash
    python manage.py generate_secret_key
    ```

4. Skopiuj nowy klucz do `.env`.

### 5. Konfiguracja Django REST Framework
W `settings.py` dodaj:
```python
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}
```

### 6. Tworzenie aplikacji `api`
```bash
python manage.py startapp api
```
Dodaj do `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...,
    "api.apps.ApiConfig",
]
```

### 7. Tworzenie modelu `Book`
W `api/models.py`:
```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    publish_date = models.DateField(blank=True, null=True)
```
Wykonaj migracje:
```bash
python manage.py makemigrations api
python manage.py migrate
```

### 8. Tworzenie serializera
W `api/serializers.py`:
```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```

### 9. Tworzenie widoków API
W `api/views.py`:
```python
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

### 10. Konfiguracja URL-i
W `api/urls.py`:
```python
from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDestroyView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
]
```
W `urls.py` projektu:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

### 11. Uruchomienie serwera Django
```bash
python manage.py runserver
```
Sprawdź API w przeglądarce lub Postmanie:
- Lista książek: [http://127.0.0.1:8000/api/books/](http://127.0.0.1:8000/api/books/)
- Szczegóły książki: [http://127.0.0.1:8000/api/books/1/](http://127.0.0.1:8000/api/books/1/)

---

## II. Konfiguracja React + Webpack

### 1. Struktura katalogów
```
frontend/
│── src/
│   ├── components/
│   │   ├── App.js
│   ├── index.js
│── static/css/
│   ├── index.css
│── templates/frontend/
│   ├── index.html
│── package.json
│── webpack.config.js
│── babel.config.json
```


### 2. Konfiguracja Babel (`babel.config.json`)
```json
{
  "presets": ["@babel/preset-env", "@babel/preset-react"]
}
```

### 3. Konfiguracja Webpack (`webpack.config.js`)
```js
const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "static/frontend"),
    filename: "main.js",
  },
  mode: "development",
  devServer: {
    static: "./static/frontend",
    port: 3000,
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: "babel-loader",
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  plugins: [new HtmlWebpackPlugin({ template: "./src/index.html" })],
};
```

### 4. Pliki źródłowe (src/)
1. src/index.js
```js
import React from "react";
import ReactDOM from "react-dom";
import App from "./components/App";
import "../static/css/index.css";

ReactDOM.render(<App />, document.getElementById("root"));
```

2. src/components/App.js
```js
import React from "react";
import { Button } from "@mui/material";

const App = () => {
  return (
    <div>
      <h1>Witaj w React!</h1>
      <Button variant="contained" color="primary">Kliknij mnie</Button>
    </div>
  );
};

export default App;
```

3. src/index.html
```html
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>React App</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>
```


### 5. Instalacja zależności
```bash
npm init -y
npm install react react-dom @mui/material @mui/icons-material @emotion/react @emotion/styled
npm install --save-dev webpack webpack-cli webpack-dev-server babel-loader @babel/core @babel/preset-env @babel/preset-react html-webpack-plugin style-loader css-loader
```

### 6. Uruchomienie Reacta
```bash
npm start
```

