from django.contrib import admin

# Register your models here.
from .models import Product,Contact,review,userorder
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(review)
admin.site.register(userorder)