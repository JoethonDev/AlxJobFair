import base64
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import HttpResponse
from jobscanner.models import Recrutier, Freelancer, ScanLog

from io import BytesIO
import qrcode
from openpyxl.drawing.image import Image

# Create your views here.
PAGE_SIZE = 10

# Helper Functions
def get_hostname(request):
    return f"{request.scheme}://{request.get_host()}"


def qr_generator(host_name: str, freelancer: Freelancer):
    url = f"{host_name}/profile/{freelancer.pk}"
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    buffer.seek(0)

    return buffer


# Home Page [Login_or_Scan]
def index(request):
    template = "index.html"
    ctx = {}
    if "is_authenticated" in request.session:
        template = "scanner.html"

    if request.method == "POST":
        login_code = request.POST.get("code", "")
        recrutier = Recrutier.objects.filter(code=login_code).first()
        if recrutier:
            request.session['is_authenticated'] = True
            request.session['recrutier_pk'] = recrutier.pk
            return redirect(reverse("home"))
        else:
            ctx['message'] = "Invalid Code!"
    
    return render(request, template, ctx)



# Profile Display [Display profile | Back Home]
def profile(request, pk):
    if "is_authenticated" in request.session:
        freelancer_profile = get_object_or_404(Freelancer, pk=pk)
        recrutier = get_object_or_404(Recrutier, pk=request.session['recrutier_pk'])
        _, created = ScanLog.objects.get_or_create(freelancer=freelancer_profile, recrutier=recrutier)
        if created:
            freelancer_profile.visits += 1
            freelancer_profile.save()

        return render(request, "profile.html", {
            "profile" : freelancer_profile,
            'comment' : _.comment
        })
    
    return redirect(reverse("home"))

def comment(request, pk):
   if "is_authenticated" in request.session:
        freelancer_profile = get_object_or_404(Freelancer, pk=pk)
        recrutier = get_object_or_404(Recrutier, pk=request.session['recrutier_pk'])
        scan_log, _ = ScanLog.objects.get_or_create(freelancer=freelancer_profile, recrutier=recrutier)
        scan_log.comment = request.POST.get("comment", "")
        scan_log.save()

        return redirect(reverse("profile", kwargs={"pk" : pk}))


def scanned(request):
    """
        Filter Scan Logs to each recrutier
        Then split into pages
        Finally return list of comments and freelancers
    """
    if "recrutier_pk" in request.session:
        recrutier = get_object_or_404(Recrutier, pk=request.session['recrutier_pk'])
        scan_log = ScanLog.objects.filter(recrutier=recrutier).order_by("pk")
        paginator = Paginator(scan_log, PAGE_SIZE)
        page_number = request.GET.get('page', "1")
        page_obj = paginator.get_page(page_number)

        return render(request, "scanned_table.html", {
            "page_obj" : page_obj
        })
    return redirect(reverse("home"))


# TODO
def dashboard(request):
    # Display a table with pagination, you can refer to scanned function and scanned_table.html
    # List 10 per page preferable to use PAGE_SIZE
    pass

# TODO
def detailed_dashboard(request, pk):
    # Here list all scanned freelancers as you wish as card or in table as you like
    # if you do pagination make sure do not make more than 10 per page and preferable to use PAGE_SIZE
    pass

# TODO
def upload_freelancers(request):
    # Take csv file From Zidan [name, email, phone_number, location, track, job_interest, cv_link]
    # Insert in Database using create of Freelancer Class
    # then generate csv file [name, email, phone, qr_code]
    # qr_code function that takes host_name and freelancer_obj to build dynamic link, is written for you, it generates buffer to use and create image then embeded it in xlsx
    host_name = get_hostname(request)
    qr_code = qr_generator(host_name, Freelancer.objects.get(pk=1))
    response = HttpResponse(content_type="image/png")
    response.content = qr_code
    return response
