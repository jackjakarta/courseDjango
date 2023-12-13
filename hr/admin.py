from django.contrib import admin
from .models import Employer, Employee, Profile
from django.contrib.auth import get_user_model

AuthUserModel = get_user_model()

# admin.site.register(Employer)
# admin.site.register(Employee)
admin.site.register(Profile)


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ("name", "get_employees_nr",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = request.user

        if user.is_superuser:
            return queryset

        return queryset.filter(owner=user)

    def get_fields(self, request, obj=None):
        all_fields = super().get_fields(request, obj)

        if not request.user.is_superuser:
            all_fields.remove('owner')

        return all_fields
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            owner = form.cleaned_data.get('owner')

            if not owner:
                obj.owner = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            if db_field.name == 'owner':
                kwargs["queryset"] = AuthUserModel.objects.filter(is_superuser=False, is_staff=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", 'employer_name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = request.user

        if user.is_superuser:
            return queryset

        return queryset.filter(employer__owner=user)
