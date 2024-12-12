from django.contrib import admin
from jobscanner.models import *
from django.utils.html import format_html
from jobscanner.models import Attendee
from django.urls import reverse
from django.db.models import Field


class AttendeModel(admin.ModelAdmin):
    search_fields = (
        "email",
        "name",
        "phone_number"
    )

    list_filter = [
        "track",
        "location"
    ]

    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'email', 'phone_number', 'track', 'cv_url'),
    #     }),
    # )

    # def get_list_display(self, request):
    #     # Dynamically include all model fields
    #     model_fields = [
    #         field.name for field in Attendee._meta.get_fields()
    #         if isinstance(field, Field)  # Only include non-relational fields
    #     ]
    #     # Add custom fields to the list display
    #     return model_fields + ['profile_link', 'qr_code']

    def profile_link(self, obj):
        # Generate a clickable link to the attendee's profile
        url = reverse("profile", kwargs={"pk": obj.pk})
        return format_html('<a href="{}" target="_blank">View Profile</a>', url)
    
    profile_link.short_description = 'Profile Link'

    def qr_code(self, obj):
        # Generate the QR code dynamically

        # Create a downloadable QR code link
        download_link = reverse("qr_code", kwargs={"pk": obj.pk})  # Custom admin URL for downloading
        return format_html(
            '<a href="{}" target="_blank">Download QR Code</a>', download_link
        )
    
    qr_code.short_description = 'QR Code'

    # def get_list_display(self, request):
    #     # Dynamically include all model fields
    #     model_fields = [field.name for field in Attendee._meta.get_fields()]
    #     # Add custom fields to the list display
    #     return model_fields + ['profile_link', 'qr_code']

    readonly_fields = ['profile_link', 'qr_code']
    # def get_readonly_fields(self, request, obj=None):
    #     # Add dynamic fields to readonly_fields
    #     readonly_fields = super().get_readonly_fields(request, obj)
    #     if obj:
    #         readonly_fields += ('profile_link', 'qr_code')
    #     return readonly_fields

# Register your models here.
admin.site.register(Attendee, AttendeModel)
admin.site.register(Recrutier)
admin.site.register(ScanLog)
