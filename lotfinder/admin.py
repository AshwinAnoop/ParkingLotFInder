#from django.contrib import admin
from django.contrib.admin import ModelAdmin,register
from django.db.models.aggregates import Avg
from .models import parkinglot,locality,booking,wallet,lotverification,extendeduser,lotSummary
from django.db.models import Count,Avg


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



@register(lotSummary)
class lotSummaryAdmin(ModelAdmin):
    change_list_template = 'admin/lot_summary_change_list.html'
    icon_name = 'event_note'
    list_filter = ('activestatus',)

    #date_hierarchy = 'created'
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        metrics = {
            'total': Count('id'),
            'average_price': Avg('price'),
        }
        response.context_data['summary'] = list(
            qs
            .values('locality')
            .annotate(**metrics)
            .order_by('-total')
        )
        #return response

        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )
        return response
