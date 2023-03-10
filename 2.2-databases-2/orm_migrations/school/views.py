from django.views.generic import ListView
from django.shortcuts import render

from .models import Student


def students_list(request):
    template = 'school/students_list.html'
    obj_list = Student.objects.all()
    context = {'object_list': obj_list}
    ordering = 'group'

    return render(request, template, context)
