from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F   # used to make changes directly into database and used to avoid race conditions
from .models import Question
import operator

def index(request):
	top_5 = Question.objects.order_by("-pub_date")[:5]
	#top_5 = ','.join([i.ques for i in top_5])
	context = {'top_5' : top_5}
	return render(request, 'polls/index.html', context)

def details(request, question_id):
	try:
		entry = Question.objects.get(pk = question_id)
		# entry = get_object_or_404(Question, pk = question_id) - alternate to all this code
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
		#return HttpResponse("Question does not exist")
	return render(request, 'polls/details.html', {'question' : entry})		

def results(request, question_id):
	q = Question.objects.get(pk = question_id)
	choices = q.choices.all()
	chosen = []
	for choice in choices:
		chosen.append((choice.choice_text, choice.votes))
	chosen.sort(key = operator.itemgetter(1), reverse = True)
	print(chosen)
	return render(request, 'polls/results.html', {'results' : chosen})			


def vote(request, question_id):
	query_ques = get_object_or_404(Question, pk = question_id)
	query_choice = request.POST['choice'][0]
	try:
		chosen = query_ques.choices.get(id = query_choice)
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/details.html', {'question' : query_ques, 'error_mssg' : "You didn't select a valid choice!"})
	else:		
		chosen.votes = F('votes') + 1  # race condition avoided
		chosen.save()
		# Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args = (question_id,)))		