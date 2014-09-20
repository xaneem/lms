from django.contrib import admin
from leave.models import Employee,Application,TransactionLog,ApplicationLog,Action,Department
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from leave.models import UserProfile

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    

admin.site.register(Employee)
admin.site.register(Application)
admin.site.register(TransactionLog)
admin.site.register(ApplicationLog)
admin.site.register(Action)
admin.site.register(Department)


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)