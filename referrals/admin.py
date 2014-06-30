from django.contrib import admin

import models

class ReferralAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('title',) }

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('title',) }

admin.site.register(models.Referral, ReferralAdmin)
admin.site.register(models.Category, CategoryAdmin)
