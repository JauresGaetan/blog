from django.contrib import admin
from django.urls import path, include  # include nécessaire pour inclure les urls des apps

urlpatterns = [
    path('admin/', admin.site.urls),

    # URLs de l'application blog
    path('blog/', include('blogs.urls')),  # Assure-toi que blogs/urls.py existe

    # URLs de l'application user (auth, profile, etc.)
    path('user/', include('users.urls')),  # Assure-toi que users/urls.py existe

    # # URLs de l'application comment
    path('comment/', include('comment.urls')),  # Assure-toi que comment/urls.py existe
]
