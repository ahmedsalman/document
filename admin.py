from django.contrib import admin

from document.models import CoAuthor, Document


class DocumentAdmin(admin.ModelAdmin):
    pass


class CoAuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(CoAuthor, CoAuthorAdmin)
admin.site.register(Document, DocumentAdmin)
