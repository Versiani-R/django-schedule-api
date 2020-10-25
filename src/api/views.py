from django.shortcuts import render
from django.http import HttpResponse

# TODO: Add a view to check which days and hours are already booked


def index(request):
    return render(request, 'api/index.html')


def api_index(request):
    return HttpResponse('Hello! You are at the /api/ index!')


# TODO: Implement a detail all ?
# TODO: Implement an id parameter ?
def api_detail(request, day=1, month=2, year=2000):
    return HttpResponse('Hello! This is the detail page!')


# TODO: Check if day, month and year are valid
# TODO: Raise 404 if no scheduled meeting with this date found
def api_schedule(request, day=1, month=2, year=2000):
    context = {
        'date': {
            'day': day,
            'month': month,
            'year': year,
        }
    }
    return render(request, 'api/schedule.html', context)


def test(request):
    return HttpResponse(f'Test')
