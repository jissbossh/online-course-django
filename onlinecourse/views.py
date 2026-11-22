from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView

from .models import Course, Lesson, Enrollment, Question, Choice, Submission


class CourseListView(ListView):
    model = Course
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'
    context_object_name = 'course'


@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('onlinecourse:course_details', pk=course_id)


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

    if request.method == 'POST':
        selected_choices = []
        for key in request.POST:
            if key.startswith('choice_'):
                selected_choices.append(int(request.POST[key]))

        submission = Submission.objects.create(enrollment=enrollment)
        submission.choices.set(Choice.objects.filter(id__in=selected_choices))
        submission.save()

        return HttpResponseRedirect(
            reverse(
                'onlinecourse:show_exam_result',
                args=(course_id, submission.id)
            )
        )

    return redirect('onlinecourse:course_details', pk=course_id)


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_ids = submission.choices.all().values_list('id', flat=True)

    total_score = 0
    questions = course.question_set.all()
    for question in questions:
        if question.is_get_score(selected_ids):
            total_score += question.grade

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        {
            'course': course,
            'submission': submission,
            'selected_ids': list(selected_ids),
            'total_score': total_score,
        },
    )