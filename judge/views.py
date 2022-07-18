import tempfile
from django.utils import timezone
import filecmp,os,shutil
from django.http import HttpResponse,HttpResponseRedirect
from .models import Problem,Solution,TestCase
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
import subprocess


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created successfully for '+ user )
            return redirect('login')
    context = {'form' : form}
    return render(request, 'judge/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password is incorrect')

		
    context={}
    return render(request, 'judge/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def index(request):
    problem_list = Problem.objects.all
    context = {'problem_list': problem_list}
    return render(request, 'judge/index.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def submit(request, problem_id):
    code=request.POST.get('solution')
    language=request.POST.get('language')
    print(language)
    sol_cpp = open('/Users/sahan/Desktop/Django/algo_oj/Project/solution.cpp', "wb+")
    sol_py = open('/Users/sahan/Desktop/Django/algo_oj/Project/solution.py', "wb+")
    if (language == "C++"):
        sol_cpp.write(str.encode(code))
        sol_cpp.seek(0)
    elif(language == "Python"):
         sol_py.write(str.encode(code))
         sol_py.seek(0)

    # temp_Solution = tempfile.NamedTemporaryFile(suffix=".cpp")
    # temp_Solution.write(str.encode(code))
    # temp_Solution.seek(0)
    # temp_Solution.close()
    problem = get_object_or_404(Problem, pk=problem_id)
    testcase = problem.testcase_set.all()
    if (language == "C++"):
        os.system('g++ /Users/sahan/Desktop/Django/algo_oj/Project/solution.cpp')
    # verdict = 'Accepted'
    for i in testcase:
        # temporary input file 
        # tempInput = tempfile.NamedTemporaryFile(suffix=".txt")
        # tempInput.write(str.encode(i.input))
        # tempInput.seek(0)
        inp = open('/Users/sahan/Desktop/Django/algo_oj/Project/inp.txt',"wb+")
        inp.write(str.encode(i.input))
        inp.seek(0)
        # temporary actual output file 
        # tempActualOutput = tempfile.NamedTemporaryFile(suffix=".txt")
        # tempActualOutput.write(str.encode(i.output))
        actual_out = open('/Users/sahan/Desktop/Django/algo_oj/Project/actual_out.txt',"wb+")
        actual_out.write(str.encode(i.output))
        actual_out.seek(0)
        # output file which we get after running the code
        # tempOutput = tempfile.NamedTemporaryFile(suffix=".txt")
        # tempOutput.seek(0)
        if (language == "C++"):
            os.system('a.exe < /Users/sahan/Desktop/Django/algo_oj/Project/inp.txt > /Users/sahan/Desktop/Django/algo_oj/Project/out.txt')
        elif (language == "Python"):
            os.system('python /Users/sahan/Desktop/Django/algo_oj/Project/solution.py < /Users/sahan/Desktop/Django/algo_oj/Project/inp.txt > /Users/sahan/Desktop/Django/algo_oj/Project/out.txt ')
        # os.system('a.exe < ' + tempInput.name + ' > ' + tempOutput.name) 
        # out = open('/Users/sahan/Desktop/Django/algo_oj/Project/out.txt',"wb+")

        # print("actual_out")
        # print(actual_out.read())
        # print("out")
        # verdict = 'Accepted'
        actual_outstring=""
        outstring=""
        out1 = '/Users/sahan/Desktop/Django/algo_oj/Project/out.txt'
        out2 = '/Users/sahan/Desktop/Django/algo_oj/Project/actual_out.txt'
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
    solution.lang = language
    sol_cpp.close()
    sol_py.close()
    solution.save()

    return redirect('submissions')

@login_required(login_url='login')
def submissions(request):
    submission = Solution.objects.all().order_by('-sub_date')
    context = {'submission': submission}
    return render(request, 'judge/submissions.html', context)
