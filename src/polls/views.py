from django.http import HttpResponse, HttpRequest, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Question

def index(request: HttpRequest ) -> HttpResponse:
    # return HttpResponse("Hello, world. You're at the polls index.")
    questions = Question.objects.order_by("-pub_date")[:5]
    # set context
    context = {
        "latest_question_list": questions
    }
    ## method 1 using loader and loader.render

    # template = loader.get_template('polls/index.html')
    # response = template.render(context, request)
    ## method 2 using render

    response = render(request, "polls/index.html", context)

    return response


def question(request: HttpRequest, question_id: int) -> HttpResponse: 
    ## method 1 using try except
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404(f"Question with id = {question_id} does not exist.")

    ## method 2 using get_object_or_404
    question = get_object_or_404(Question, pk=question_id)

    
    return HttpResponse(render(request, "polls/question.html", {"question":question}))

def results(request: HttpRequest, question_id: int) -> HttpResponse:
    return HttpResponse(f"You're looking at the results of question {question_id}")

def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    return HttpResponse(f"You're voting on question {question_id}")
