import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

months2str = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

class ConfForm(forms.Form):
    name = forms.CharField(max_length=200)
    day = forms.IntegerField(min_value=1, max_value=31)
    month = forms.IntegerField(min_value=1, max_value=12)


# Create your views here.
def index(request):
    if 'name' not in request.session:
        return redirect('birthday:conf', permanent=True)
    else:
        date = datetime.datetime.now()
        day = request.session.get('day')
        month = request.session.get('month')
        return render(request, 'birthday/index.html', {
            'birthday': date.day == day and date.month == month,
            'name': request.session.get('name'),
            'day': day,
            'month': months2str[month]
        })

def conf(request):
    print('name' in request.session)
    if 'name' in request.session:
        return redirect('birthday:index', permanent=True)

    context = {}

    if request.method == 'POST':
        form = ConfForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            month = form.cleaned_data['month']
            day = request.session['day'] = form.cleaned_data['day']
            not_valid = True

            if day_validator( int(day), int(month)):
                request.session['name'] = name
                request.session['month'] = month
                request.session['day'] = day
                return HttpResponseRedirect(reverse('birthday:index'))
            else:
                context['not_valid'] = not_valid
                context['form'] = ConfForm()
                return render(request, 'birthday/conf.html', context)

    context['form'] = ConfForm()
    return render(request, 'birthday/conf.html', context)


#Functions
def day_validator(day:int, month:int) -> bool:
    bisiesto_compa = month%4
    bisiesto_compb = month%100
    bisiesto_compc = month%400
    bisiesto = bisiesto_compa and (bisiesto_compb or bisiesto_compc)

    large_month = [1,3,5,7,8,10,12]
    validate_day: tuple = ()

    if (month in large_month and day < 31) or (month not in large_month and day < 30):
        validate_day = (day, month)
    elif month == 2:
        if bisiesto and day <= 29:
            validate_day = (day, month)
        elif day <= 28:
            validate_day = (day, month)
    else:
        validate_day = None
    
    return validate_day