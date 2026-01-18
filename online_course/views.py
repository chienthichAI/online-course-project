from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Question, Choice, Submission, Enrollment


def submit(request, course_id):
    model = Course
    template_name = 'online_course/course_details_bootstrap.html'
    course = get_object_or_404(model, pk=course_id)

    if request.method == 'POST':
        selected_ids = request.POST.getlist('choice')
        if len(selected_ids) == 0:
            return HttpResponseRedirect(reverse('online_course:course_details', args=(course.id,)))
        
        # Create a new submission
        # In a real app, we would link this to the user's enrollment
        # For this standalone submission, we'll create a dummy submission object
        # to satisfy the requirement of using the Submission model
        submission = Submission.objects.create(enrollment=None) # Passing None as we don't have active enrollments
        
        # Add selected choices to the submission
        for choice_id in selected_ids:
            try:
                choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(choice)
            except Choice.DoesNotExist:
                pass
        
        submission.save()
        
        return render(request, 'online_course/exam_result_bootstrap.html', {'course': course, 'submission': submission})
            
    return render(request, template_name, {'course': course})

def show_exam_result(request, course_id, submission_id):
    context = {}
    context['course'] = get_object_or_404(Course, pk=course_id)
    context['submission'] = get_object_or_404(Submission, pk=submission_id)
    return render(request, 'online_course/exam_result_bootstrap.html', context)
