from ajax_select import register, LookupChannel
from .models import Person

@register('persons')
class PersonsLookup(LookupChannel):

    model = Person

    def get_query(self, q, request):
        names = q.split(",",1)
        last_name = names[0].strip()
        if(len(names)>1):
            first_name = names[1].strip()
            return self.model.objects.filter(last_name__icontains=last_name, first_name__contains=first_name).order_by('last_name')
        else:
            return self.model.objects.filter(last_name__icontains=last_name).order_by('last_name')
