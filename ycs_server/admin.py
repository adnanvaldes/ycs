from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.http.response import HttpResponse
from .models import UserSettings


# Register your models here.
class HomePageAdmin(admin.ModelAdmin):
    def add_view(self, request):
        if request.method == "POST":
            # Assuming you want a single, global HomePage object
            if UserSettings.objects.count() > 1:
                # redirect to a page saying
                # you can't create more than one
                return HttpResponse("foo")
        return super(HomePageAdmin, self).add_view(request)

# ...

admin.site.register(UserSettings, HomePageAdmin)