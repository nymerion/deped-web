from django.db.models import Count
from vacancy.models import Position


def generate_vacancy_context(vacancy, context):
    vc = {
        'publish_date': vacancy.publish_date,
        'positions': []
    }
    positions = vacancy.items.filter(filled=False).order_by('-position').values('position').annotate(count=Count('position'))

    # group by positions
    for pd in positions:
        position = Position.objects.get(pk=pd['position'])
        station_types = vacancy.items.filter(position=position).values('station_type').annotate(count=Count('station_type'))

        # group by station type
        for st in station_types:
            stations = vacancy.items.filter(position=position, station_type=st['station_type']).values('station_name').annotate(count=Count('station_name'))
            
            # group by station name
            for station in stations:
                items = vacancy.items.filter(position=position, station_type=st['station_type'], station_name=station['station_name']).order_by('number')
                vc['positions'].append({  'name': position.name,
                        'station_type': 'High School' if st['station_type']=='HS' else ('Elementary' if st['station_type']=='ES' else 'Division Office'),
                        'station_name': station['station_name'],
                        'salary_grade': position.salary_grade,
                        'qualifications': position.qualification_standards.all(),
                        'qs_count': len(position.qualification_standards.all()),
                        'items': items,
                        'count': len(items),
                })

    context['vacancies'].append(vc)
