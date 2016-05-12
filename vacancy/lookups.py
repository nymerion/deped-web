from ajax_select import register, LookupChannel
from django.db.models import Q
from .models import Person

@register('persons')
class PersonsLookup(LookupChannel):

    model = Person

    def get_query(self, q, request):
        if ',' in q:
            names = q.split(",")
            last_name = names[0].strip()
            del names[0]
        else:
            names = q.split(" ")
            while not names[-1]:
                del names[-1]
            last_name = names[-1].strip()
            del names[-1]
        first_name = " ".join([name.strip() for name in names if name ])
        
        if first_name:
            first_name = first_name.strip()
            results = self.model.objects.filter(last_name__icontains=last_name, first_name__icontains=first_name).order_by('last_name')
        else:
            results = self.model.objects.filter(Q(last_name__icontains=last_name)|Q(first_name__icontains=last_name)).order_by('last_name')

        return results
