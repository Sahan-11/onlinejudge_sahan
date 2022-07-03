from django.http import HttpResponse
from .models import Problem,Solution,TestCase
from django.shortcuts import get_object_or_404, render

def index(request):
    problem_list = Problem.objects.all
    context = {'problem_list': problem_list}
    return render(request, 'judge/index.html', context)

def detail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request, 'judge/detail.html', {'problem': problem})