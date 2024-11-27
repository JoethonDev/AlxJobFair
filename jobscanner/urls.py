from django.urls import path
from jobscanner.views import *

urlpatterns = [
    path("", index, name="home"),
    path("scanned", scanned, name="scanned"),
    path("comment/<int:pk>", comment, name="comment"),
    path("profile/<int:pk>", profile, name="profile"),
    # TODO
    path("dashboard", dashboard, name="dashboard"),
    path("dashboard/<int:pk>", detailed_dashboard, name="detailed_dashboard"),
    path("upload", upload_freelancers, name="upload"),
]