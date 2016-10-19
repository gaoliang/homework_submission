from django.contrib.auth.decorators import permission_required, login_required
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from submission_system.models import Homework, Courser, HomeworkAnswer


def index_view(request):
    return render(request, template_name='index_page.html', context={})


@permission_required('submission_system.add_homework')
def add_homework(request, courser_name_en):
    """
    新建作业
    """
    if request.method == 'POST':
        homework = Homework(name=request.POST['name'], content=request.POST['content'],
                            courser=Courser.objects.get(name_en=courser_name_en))
        homework.save()
        return redirect(reverse('homework_detail', args=(homework.pk,)))
    else:
        return render(request, template_name='add_homework.html', context={'courser': Courser.objects.get(
            name_en=courser_name_en)})


def list_homework(request, courser_name_en):
    return render(request, 'homework_list.html',
                  context={'courser_name_en': courser_name_en,
                           'courser': Courser.objects.get(name_en=courser_name_en)})


def get_homework_list(request, courser_name_en):
    json_data = {}
    recodes = []
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    homeworks = Homework.objects.filter(courser__name_en=courser_name_en)
    json_data['total'] = homeworks.count()
    for homework in homeworks.all()[offset:offset + limit]:
        recodes.append({'name': homework.name, 'finished_num': homework.homeworkanswer_set.count(), 'id': homework.id})
    json_data['rows'] = recodes
    return JsonResponse(json_data)


def homework_detail(request, homework_id):
    homework = Homework.objects.get(pk=homework_id)
    return render(request, 'homework_detail.html', context={'homework': homework, })


@permission_required('submission_system.add_homework')
def get_finished(request, homework_id):
    json_data = {}
    recodes = []
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    submissions = HomeworkAnswer.objects.filter(homework__pk=homework_id)
    json_data['total'] = submissions.count()
    for submission in submissions.all()[offset:offset + limit]:
        recodes.append({'name': submission.creator.username, 'id_num': submission.creator.id_num, 'id': submission.pk})
        json_data['rows'] = recodes
    return JsonResponse(json_data)


@login_required
def add_submission(request, homework_id):
    if request.method == 'POST':
        file = request.FILES.get('picture')
        if file:
            file.name = 'ppp'
        submission = HomeworkAnswer(code=request.POST['code'], content=request.POST['content'],
                                    homework=Homework.objects.get(pk=homework_id),picture=file)
        submission.save()
        submission.creator = request.user
        print(submission.creator)
        submission.save()
        return redirect(reverse('submission_detail', args=(submission.id,)))
    else:
        return render(request, 'add_submission.html',
                      context={'homework': Homework.objects.get(pk=homework_id)})


def submission_detail(request, submission_id):
    if HomeworkAnswer.objects.get(pk=submission_id).creator != request.user and not request.user.is_superuser:
        raise Http404
    return render(request, 'submission_detail.html',
                  context={'submission': HomeworkAnswer.objects.get(pk=submission_id)})

def get_my_submissions(request):
    json_data = {}
    recodes = []
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    submissions = HomeworkAnswer.objects.filter(creator=request.user)
    json_data['total'] = submissions.count()
    for submission in submissions.all()[offset:offset + limit]:
        recodes.append({'homework':submission.homework.name, 'courser': submission.homework.courser.name, 'id':submission.pk})
    json_data['rows'] = recodes
    return JsonResponse(json_data)


def list_my_submissions(request):
    return render(request,"list_my_submission.html")
