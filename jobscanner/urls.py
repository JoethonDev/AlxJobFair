from django.urls import path
from jobscanner.views import *

urlpatterns = [
    path("", index, name="home"),
    path("scanned/", scanned, name="scanned"),
    path("comment/<uuid:pk>", comment, name="comment"),
    path("profile/<uuid:pk>", profile, name="profile"),
    # TODO
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/<int:pk>", detailed_dashboard, name="detailed_dashboard"),
    path("upload/freelancer/", upload_freelancers, name="upload_freelancer"),
    path("upload/recrutier/", upload_recrutiers, name="upload_recrutier"),
    path("download-leads/", download_leads, name="download_leads")
]