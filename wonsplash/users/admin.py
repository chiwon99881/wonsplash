from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from wonsplash.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("avatar", "following", "followers")}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["id","username", "is_superuser"]
    list_display_links = ["id","username"]
    search_fields = ["username"]
    list_filter = ["id","username"]
