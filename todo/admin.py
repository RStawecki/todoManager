from django.contrib import admin
from todo.models import Todo


class createDate(admin.ModelAdmin):
    readonly_fields = ('createDate',)

admin.site.register(Todo, createDate)