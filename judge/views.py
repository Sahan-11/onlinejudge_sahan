import tempfile
from django.utils import timezone
import filecmp,os,shutil
from django.http import HttpResponse,HttpResponseRedirect
from .models import Problem,Solution,TestCase
from django.shortcuts import get_object_or_404, render, redirect

def index(request):
    problem_list = Problem.objects.all
    context = {'problem_list': problem_list}
    return render(request, 'judge/index.html', context)

def detail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request, 'judge/detail.html', {'problem': problem})

# def submit(request, problem_id):
#     f = request.FILES['solution']
#     with open('/Users/sahan/Desktop/Project/solution.cpp', 'wb+') as dest:
#         for chunk in f.chunks():
#             dest.write(chunk)
        
#     sol = open('/Users/sahan/Desktop/Project/solution.cpp', "r")
#     os.system('g++ /Users/sahan/Desktop/Project/solution.cpp')
#     os.system('a.exe < /Users/sahan/Desktop/Project/inp.txt > /Users/sahan/Desktop/Project/out.txt')

#     out1 = '/Users/sahan/Desktop/Project/out.txt'
#     out2 = '/Users/sahan/Desktop/Project/actual_out.txt'

#     if(filecmp.cmp(out1, out2, shallow=False)):
#         verdict = 'Accepted'
#     else:
#         verdict = 'Wrong Answer'

#     solution = Solution()
#     solution.problem = Problem.objects.get(pk=problem_id)
#     solution.verdict = verdict
#     solution.sub_date = timezone.now()
#     solution.sub_code = sol.read()
#     solution.save()

#     return redirect('submissions')

def submit(request, problem_id):
    code=request.POST.get('solution')
    language=request.POST.get('language')
    sol = open('/Users/sahan/Desktop/Project/solution.cpp', "wb+")
    sol.write(str.encode(code))
    sol.seek(0)
    # temp_Solution = tempfile.NamedTemporaryFile(suffix=".cpp")
    # temp_Solution.write(str.encode(code))
    # temp_Solution.seek(0)
    # temp_Solution.close()
    problem = get_object_or_404(Problem, pk=problem_id)
    testcase = problem.testcase_set.all()
    os.system('g++ /Users/sahan/Desktop/Project/solution.cpp')
    # verdict = 'Accepted'
    for i in testcase:
        # temporary input file 
        # tempInput = tempfile.NamedTemporaryFile(suffix=".txt")
        # tempInput.write(str.encode(i.input))
        # tempInput.seek(0)
        inp = open('/Users/sahan/Desktop/Project/inp.txt',"wb+")
        inp.write(str.encode(i.input))
        inp.seek(0)
        # temporary actual output file 
        # tempActualOutput = tempfile.NamedTemporaryFile(suffix=".txt")
        # tempActualOutput.write(str.encode(i.output))
        actual_out = open('/Users/sahan/Desktop/Project/actual_out.txt',"wb+")
        actual_out.write(str.encode(i.output))
        actual_out.seek(0)
        # output file which we get after running the code
        # tempOutput = tempfile.NamedTemporaryFile(suffix=".txt")
        # tempOutput.seek(0)
        os.system('a.exe < /Users/sahan/Desktop/Project/inp.txt > /Users/sahan/Desktop/Project/out.txt')
        # os.system('a.exe < ' + tempInput.name + ' > ' + tempOutput.name) 
        # out = open('/Users/sahan/Desktop/Project/out.txt',"wb+")

        # print("actual_out")
        # print(actual_out.read())
        # print("out")
        # verdict = 'Accepted'
        actual_outstring=""
        outstring=""
        out1 = '/Users/sahan/Desktop/Project/out.txt'
        out2 = '/Users/sahan/Desktop/Project/actual_out.txt'
        with open(out1,'r') as var:
            for line in var:
                line=line.replace('/r',' ')
                outstring=outstring+line

        with open(out2,'r') as var:
            for line in var:
                line=line.replace('/r',' ')
                actual_outstring=actual_outstring+line
        
        # print(actual_outstring)
        # print(outstring)
        if(actual_outstring.strip() == outstring.strip()):
            verdict = 'Accepted'
        else:
            verdict = 'Wrong Answer'
        
        actual_out.close()
        inp.close()

    solution = Solution()
    solution.problem = Problem.objects.get(pk=problem_id)
    solution.verdict = verdict
    solution.sub_date = timezone.now()
    solution.sub_code = code
    sol.close()
    solution.save()

    return redirect('submissions')


def submissions(request):
    submission = Solution.objects.all().order_by('-sub_date')
    context = {'submission': submission}
    return render(request, 'judge/submissions.html', context)
