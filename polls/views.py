from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question, Comments
from array import array
from .forms import CommentFrom

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise get_object_or_404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))

def show_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    comments = Comments.objects.filter(comments_question=question_id)
    form = OrderForm(request.POST or None, initial={"polls":question})
    form_comments = CommentForm

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('{}?sended=True'.format(reverse))

    return render(request, 'polls/results.html', {
        'question': question,
        'comments': comments,
        'form': form,
        'form_commets': form_comments,
        'sended': request.GET.get('sended', False)
    })

def addcomment(request, article_id):
    if request.method == "POST" and ("pause" not in request.session):
     form = CommentFrom(request.POST)
     if form.is_valid():
             comment = form.save(commit=False)
             comment.comments_article = Article.objects.get(id=question_id)
             form.save()
             request.session.set_expiry(60)
             request.session["pause"] = True
     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))