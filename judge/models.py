from django.db import models

class Problem(models.Model):
    statement = models.TextField()
    name = models.CharField(max_length=200)
    code = models.TextField()
    difficulty = models.CharField(max_length=200)

class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=200)
    sub_date = models.DateTimeField('date published') #submission date and time
    
class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input = models.TextField()
    output = models.TextField()

