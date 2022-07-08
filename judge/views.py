from django.utils import timezone
import filecmp,os
from django.http import HttpResponse,HttpResponseRedirect
from .models import Problem,Solution,TestCase
from django.shortcuts import get_object_or_404, render

def index(request):
    problem_list = Problem.objects.all
    context = {'problem_list': problem_list}
    return render(request, 'judge/index.html', context)

def detail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request, 'judge/detail.html', {'problem': problem})

def submit(request, problem_id):
    f = request.FILES['solution']
    with open('/Users/sahan/Desktop/Project/solution.cpp', 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
        
    sol = open('/Users/sahan/Desktop/Project/solution.cpp', "r")
    os.system('g++ /Users/sahan/Desktop/Project/solution.cpp')
    os.system('a.exe < /Users/sahan/Desktop/Project/inp.txt > /Users/sahan/Desktop/Project/out.txt')

    out1 = '/Users/sahan/Desktop/Project/out.txt'
    out2 = '/Users/sahan/Desktop/Project/actual_out.txt'

    if(filecmp.cmp(out1, out2, shallow=False)):
        verdict = 'Accepted'
    else:
        verdict = 'Wrong Answer'

    solution = Solution()
    solution.problem = Problem.objects.get(pk=problem_id)
    solution.verdict = verdict
    solution.sub_date = timezone.now()
    solution.sub_code = sol.read()
    solution.save()

    return HttpResponse(verdict)

