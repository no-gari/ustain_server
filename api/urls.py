from django.urls import path, include

urlpatterns = [
    path('user/', include('api.user.urls')),
    path('firebase/', include('api.firebase.urls')),
    path('magazine/', include('api.magazine.urls')),
    path('commerce/', include('api.commerce.urls')),
]
