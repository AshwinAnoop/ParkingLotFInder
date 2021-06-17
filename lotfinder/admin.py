#from django.contrib import admin
from django.contrib.admin import ModelAdmin,register
from .models import parkinglot,locality,booking,wallet,lotverification,extendeduser


# Register your models here.

#admin.site.register(parkinglot)
#admin.site.register(locality)

@register(locality)
class localityAdmin(ModelAdmin):
    list_display = ('id', 'locality')
    icon_name = 'add_location'

@register(parkinglot)
class parkinglotAdmin(ModelAdmin):
    list_display = ('id','locality','get_name','get_userid','title','price','monthlyrent','verifystatus','activestatus','bookedstatus')
    icon_name = 'local_car_wash'
    list_filter = ('bookedstatus','activestatus','monthlyrent',)

    def get_name(self, obj):
        return obj.userid.first_name
    get_name.admin_order_field  = 'userid'  #Allows column order sorting
    get_name.short_description = 'User Name'  #Renames column head
    def get_userid(self, obj):
        return obj.userid.id
    get_userid.short_description = 'User ID'

@register(booking)
class bookingAdmin(ModelAdmin):
    list_display = ('id','booktime','vacate','lotid','get_name','get_userid','payment', 'paymentstatus','monthlysubscribe')
    icon_name = 'assessment'
    list_filter = ('paymentstatus','monthlysubscribe','lotid')

    def get_name(self, obj):
        return obj.userid.first_name
    get_name.admin_order_field  = 'userid'  #Allows column order sorting
    get_name.short_description = 'User Name'  #Renames column head
    def get_userid(self, obj):
        return obj.userid.id
    get_userid.short_description = 'User ID'

@register(wallet)
class walletAdmin(ModelAdmin):
    list_display = ('id','get_name','get_userid','amount', 'Transactdate')
    icon_name = 'monetization_on'
    def get_name(self, obj):
        return obj.userid.first_name
    get_name.admin_order_field  = 'userid'  #Allows column order sorting
    get_name.short_description = 'User Name'  #Renames column head
    def get_userid(self, obj):
        return obj.userid.id
    get_userid.admin_order_field  = 'userid'  #Allows column order sorting
    get_userid.short_description = 'User ID'  #Renames column head

@register(lotverification)
class lotverificationAdmin(ModelAdmin):
    list_display = ('id','lotid','get_name','get_verid','verifydate','allotedstatus')
    icon_name = 'check_box'
    list_filter = ('allotedstatus','verifydate',)

    def get_name(self, obj):
        return obj.verifier.first_name
    get_name.admin_order_field  = 'verifier'  #Allows column order sorting
    get_name.short_description = 'Verifier Name'  #Renames column head
    def get_verid(self, obj):
        return obj.verifier.id
    get_verid.admin_order_field  = 'verifier'  #Allows column order sorting
    get_verid.short_description = 'Verifier ID'  #Renames column head


@register(extendeduser)
class extendeduserAdmin(ModelAdmin):
    list_display = ('get_userid','get_name','mobile', 'walletbalance')
    icon_name = 'contact_phone'

    def get_name(self, obj):
        return obj.user.first_name
    get_name.admin_order_field  = 'user'  #Allows column order sorting
    get_name.short_description = 'User Name'  #Renames column head
    def get_userid(self, obj):
        return obj.user.id
    get_userid.admin_order_field  = 'user'  #Allows column order sorting
    get_userid.short_description = 'User ID'  #Renames column head


