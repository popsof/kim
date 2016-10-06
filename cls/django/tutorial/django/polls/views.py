from django.shortcuts import get_object_or_404, render

# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import loader
from django.urls import reverse

from .models import Question

def index(request):
	q_list = Question.objects.order_by( '-pub_date' )[:5]
	context = {
		'q_list': q_list,
	}
	return render( request, 'index.html', context )

def index_old(request):
	q_list = Question.objects.order_by( '-pub_date' )[:5]
	template = loader.get_template( 'index.html' )
	context = {
		'q_list': q_list,
	}
	return HttpResponse( template.render( context, request ) )
#	output = '<br>\n'.join( [q.question_text for q in q_list] )
#	return HttpResponse( output )

#	return HttpResponse( "Hello, world. You're at the polls index." )

def detail( request, q_id ):
	q = get_object_or_404( Question, pk=q_id )
	return render( request, 'detail.html', {'question':q } )

def detail_old(request, q_id ):
	try:
		q = Question.objects.get( pk=q_id )
	except Question.DoesNotExist:
		raise Http404( "Question does not exist" )
	return render( request, 'detail.html', {'question':q } )

#	return HttpResponse( "You're looking at question {}.".format( q_id ) )


def results(request, q_id ):
	q = get_object_or_404( Question, pk=q_id )
	return render( request, 'results.html', { 'question':q } )

#	return HttpResponse( "You're looking at the results of question {}.".format( q_id ) )

def vote( request, q_id ):
	question = get_object_or_404( Question, pk=q_id )
	try:
		selected_choice = question.choice_set.get( pk=request.POST['choice'] )
	except( KeyError, Choice.DoesNotExist ):
		con = {
			'question': question,
			'error_message': "You didn't select a choice.",
		}
		return render( request, 'detail.html', con )
	else:
		selected_choice.votes += 1
		selected_choice.save()

		return HttpResponseRedirect(
					 reverse( 'polls:results', args=(question.id,) ) )

#	return HttpResponse( "You're voting on question {}.".format( q_id ) )

def add_choice( request, q_id ):
	question = get_object_or_404( Question, pk=q_id )
	try:
		choice_name = request.POST['new_choice']
	except KeyError:
		con = {
			'question': question,
			'error_message': "You didn't input new choice.",
		}
		return render( request, 'detail.html', con )

	nameLen = len(choice_name)
	if nameLen <= 0 or nameLen > 200:
		con = {
			'question': question,
			'error_message': "You didn't input valid choice.",
		}
		return render( request, 'detail.html', con )

	choice_list = question.choice_set.filter( choice_text=choice_name )
	choice_count = len(choice_list)
	if choice_count != 0:
		con = {
			'question': question,
			'error_message': "Same choice[{}] already exist!!! LOOK AGAIN!!!".
								format( choice_name ),
		}
		return render( request, 'detail.html', con )
	
	c = question.choice_set.create( choice_text=choice_name, votes=0 )
	
	return HttpResponseRedirect(
					 reverse( 'polls:detail', args=(question.id,) ) )


