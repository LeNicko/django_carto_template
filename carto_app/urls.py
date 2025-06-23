from django.urls import path
from .views import impact_serveur, requete_sql, visualisation, visualisation_data  

urlpatterns = [
    path('', impact_serveur, name='impact_serveur'),
    path('sql/', requete_sql, name='requete_sql'),
    path('visualisation/', visualisation, name='visualisation'),
    path('api/visualisation/', visualisation_data, name='visualisation_data'),
]


