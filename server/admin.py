from django.contrib import admin
from server.models import user_registration, main_data

class DataAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_email', 'user_password')
admin.site.register(user_registration, DataAdmin)

class data_full(admin.ModelAdmin):
    list_display = ('id', 'Institute','Academic_Program_Name','Seat_Type','Gender','Opening_Rank','Closing_Rank','Year','Round')
admin.site.register(main_data, data_full)
