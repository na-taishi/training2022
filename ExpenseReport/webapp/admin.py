from django.contrib import admin
from .models import Account
from .models import ExpenseReport
from .models import Route
from .models import Transportation
from .models import Subjects


# Register your models here.
admin.site.register(Account)
admin.site.register(ExpenseReport)
admin.site.register(Route)
admin.site.register(Transportation)
admin.site.register(Subjects)