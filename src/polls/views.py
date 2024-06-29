from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.urls import reverse

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

    question = get_object_or_404(Question, pk=question_id)

    return render(request, "polls/results.html", {"question": question})


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(
            pk=request.POST["choice"]
        )
    except KeyError:
        return render(request, "polls/question.html", {
            "question": question,
            "error_message": "You didn't select a choice."
        })
    else:
        selected_choice.votes = F("votes") +1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results",
                                            args=(question.id,)))
