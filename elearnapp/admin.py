from django.contrib import admin
from .models import CustomUser, Course, Assignment, Submission

# Register models in Django Admin
admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Submission)
