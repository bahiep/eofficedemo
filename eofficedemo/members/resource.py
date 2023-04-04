from import_export import resources
from django.contrib.auth.models import User

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'password','last_login','is_superuser','username','last_name','email','is_staff','is_active','date_joind','first_name')
        # fields = ('id','username', 'first_name', 'last_name','email')