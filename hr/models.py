from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

AuthUserModel = get_user_model()


class MyModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Employer(MyModel):
    class Meta:
        db_table = "employers"

    name = models.CharField(max_length=250, unique=True, null=False)
    owner = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, null=False, default=2)
    employees = models.ManyToManyField(AuthUserModel, through="Employee", related_name="employees")

    def __str__(self):
        return self.name

    def get_employees_nr(self):
        return self.employees.count()


class Employee(MyModel):
    class Meta:
        db_table = "employees"

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    wage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100,
        null=False,
        validators=[MinValueValidator(0.00)]
    )

    def __str__(self):
        return self.user.email

    def first_name(self):
        return self.user.first_name

    first_name.short_description = 'First Name'
    first_name.ordered_field = "user__first_name"

    def last_name(self):
        return self.user.last_name

    last_name.short_description = 'last Name'
    last_name.ordered_field = "user__last_name"

    def employer_name(self):
        return self.employer.name

    employer_name.short_description = 'Employer Name'
    employer_name.ordered_field = "employer__name"


class Profile(MyModel):
    class Meta:
        db_table = "profiles"

    user = models.OneToOneField(AuthUserModel, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="profiles", null=True, default=None)

    def __str__(self):
        return str(self.user)
