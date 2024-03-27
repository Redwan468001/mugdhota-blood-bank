from django.contrib import admin
from .models import User, Donner, Blood, Location, Division, Contact, BloodInfoAddProblem, ManagementRole, Management

# Register your models here.
@admin.register(User)
class UserDetails(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'joined']
    search_fields = ("name", "phone", "name", "email")
    list_filter = ('joined',)
    list_editable = ('phone',)

    
@admin.register(Donner)
class DonnerDetails(admin.ModelAdmin):
    list_display = ['name', 'bloodgroups', 'location', 'phone', 'donation_date', 'status', 'author', 'updated']
    search_fields = ("name", "phone")
    list_filter = ('location', 'bloodgroups',)
    list_editable = ('location', 'phone', 'status')
    field = ['Questions_text', 'status']
    actions = ['verified_donner', 'not_verified_donner']

    def verified_donner(self,request,queryset):
        queryset.update(status = 'Verified Donner')

    def not_verified_donner(self,request,queryset):
        queryset.update(status = 'Not Verified Donner')
        
    def get_queryset(self, request):
        queryset = super(DonnerDetails, self).get_queryset(request)
        queryset = queryset.order_by('-updated')
        return queryset


#Contact Us
@admin.register(Contact)
class contactdetails(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'question', 'created', 'cntstatus']
    search_fields = ("name__startswith", "phone__startswith", "name", "email")
    list_filter = ('created', 'cntstatus',)
    list_editable = ('phone', 'cntstatus')
    field = ['Questions_text', 'cntstatus']
    actions = ['Solved', 'Unsolved']
    
    def Solved(self,request,queryset):
        queryset.update(cntstatus = 'Solved')

    def Unsolved(self,request,queryset):
        queryset.update(cntstatus = 'Unsolved')


#Blood Info Add Problem
@admin.register(BloodInfoAddProblem)
class problemdetails(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'question', 'created', 'biapstatus']
    search_fields = ("name__startswith", "phone__startswith", "name", "email")
    list_filter = ('created', 'biapstatus',)
    list_editable = ('phone', 'biapstatus')
    field = ['Questions_text', 'biapstatus']
    actions = ['Solved', 'Unsolved']
    
    def Solved(self,request,queryset):
        queryset.update(biapstatus = 'Solved')

    def Unsolved(self,request,queryset):
        queryset.update(biapstatus = 'Unsolved')


admin.site.register(Blood)
admin.site.register(Location)
admin.site.register(Division)
admin.site.register(ManagementRole)

#Contact Us
@admin.register(Management)
class managementdetails(admin.ModelAdmin):
    list_display = ['serial_num', 'name', 'management_role', 'email', 'phone', 'joined']
    
    def get_queryset(self, request):
        queryset = super(managementdetails, self).get_queryset(request)
        queryset = queryset.order_by('serial_num')
        return queryset




