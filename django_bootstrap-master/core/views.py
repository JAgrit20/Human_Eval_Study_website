from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Todo
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from django.shortcuts import render
from .models import Todo 
def index(request):
    return render(request, 'index.html', {})
def examples(request):
    return render(request, 'examp.html', {})
def team(request):
    return render(request, 'team.html', {})
def home(request):
    BUG_REPORT_CONDITIONS = {
        'normal': {
            'url': 'https://bugwise.shaktilab.org/report_it',
            'text': 'File Bug Report',
            'class': 'bug-btn normal'
        },
        'ai': {
            'url': 'https://bugwise.shaktilab.org/research', # Assuming this is the AI version URL
            'text': 'File Bug Report with AI',
            'class': 'bug-btn ai'
        }
    }

    # Check if a condition is already assigned in the session
    assigned_condition_key = request.session.get('bug_report_condition')

    if assigned_condition_key not in BUG_REPORT_CONDITIONS:
        # If no valid condition assigned, randomly choose one
        assigned_condition_key = random.choice(list(BUG_REPORT_CONDITIONS.keys()))
        # Store the assigned condition in the session for persistence
        request.session['bug_report_condition'] = assigned_condition_key
        print(f"User {request.session.session_key}: Assigned bug report condition '{assigned_condition_key}'") # For debugging

    # Retrieve the details for the assigned condition
    assigned_condition_details = BUG_REPORT_CONDITIONS[assigned_condition_key]

    # Prepare button details for the template
    # **IMPORTANT for Tracking**: Add the condition as a URL parameter
    # The external site needs to be able to capture this 'condition' parameter.
    button_url_with_tracking = f"{assigned_condition_details['url']}?condition={assigned_condition_key}"

    button_context = {
        'bug_report_url': button_url_with_tracking,
        'bug_report_text': assigned_condition_details['text'],
        'bug_report_class': assigned_condition_details['class'],
        'bug_report_condition': assigned_condition_key # Pass the key if needed elsewhere
    }

    # --- End Bug Report Randomization Logic ---

    # Fetch Todos (your existing logic)
    todos = Todo.objects.all().order_by('-created_at')

    # Combine contexts and render
    context = {
        'todos': todos,
        **button_context # Merge the button context variables
    }
    return render(request, 'home.html', context)
    # todos = Todo.objects.all().order_by('-created_at')
    # return render(request, 'home.html', {'todos': todos})

@csrf_exempt
def add_todo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        if title:
            todo = Todo.objects.create(title=title)
            return JsonResponse({
                'id': todo.id,
                'title': todo.title,
                'completed': todo.completed,
                'created_at': todo.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
    return JsonResponse({'error': 'Invalid data'}, status=400)

@csrf_exempt
def toggle_todo(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        todo.completed = not todo.completed
        todo.save()
        return JsonResponse({'success': True, 'completed': todo.completed})
    except Todo.DoesNotExist:
        return JsonResponse({'error': 'Todo not found'}, status=404)

@csrf_exempt
def delete_todo(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        todo.delete()
        return JsonResponse({'success': True})
    except Todo.DoesNotExist:
        return JsonResponse({'error': 'Todo not found'}, status=404)