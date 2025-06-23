from django.shortcuts import render
from django.db import connection
from .models import Serveur, Application, BaseDeDonnees
from django.http import JsonResponse
from .models import ServiceMetier, AppServiceMetier


def impact_serveur(request):
    serveurs = Serveur.objects.all()
    serveur_id = request.GET.get("serveur_id")
    selected = None
    applications = []
    bdds = []

    if serveur_id:
        try:
            selected = Serveur.objects.get(id=serveur_id)
            applications = Application.objects.filter(serveur=selected)
            bdds = BaseDeDonnees.objects.filter(serveur=selected)
        except Serveur.DoesNotExist:
            pass

    return render(request, "impact.html", {
        "serveurs": serveurs,
        "selected": selected,
        "applications": applications,
        "bdds": bdds,
    })

def requete_sql(request):
    result = []
    headers = []
    sql = ""
    error = None

    if request.method == "POST":
        sql = request.POST.get("sql", "")
        if sql.strip().lower().startswith("select"):
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    headers = [col[0] for col in cursor.description]
                    result = cursor.fetchall()
            except Exception as e:
                error = str(e)
        else:
            error = "Seules les requêtes SELECT sont autorisées."

    return render(request, "requete_sql.html", {
        "sql": sql,
        "headers": headers,
        "result": result,
        "error": error
    })

def visualisation(request):
    return render(request, "visualisation.html")

def visualisation_data(request):
    serveur_filtre = request.GET.get("serveur")
    data = []

    serveurs = Serveur.objects.all()
    if serveur_filtre:
        serveurs = serveurs.filter(nom=serveur_filtre)

    for serveur in serveurs:
        apps = []
        for app in Application.objects.filter(serveur=serveur):
            services = ServiceMetier.objects.filter(
                id__in=AppServiceMetier.objects.filter(application=app).values_list('service_metier_id', flat=True)
            )
            apps.append({
                "nom": app.nom,
                "version": app.version,
                "services": [s.nom for s in services]
            })
        data.append({
            "serveur": serveur.nom,
            "applications": apps
        })

    return JsonResponse(data, safe=False)
