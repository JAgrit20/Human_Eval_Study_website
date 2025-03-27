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
import random
from django.shortcuts import render

def home(request):
    BUG_REPORT_CONDITIONS = {
        'normal': {
            'url': 'https://bugwise.shaktilab.org/report_it',
            'text': 'File Bug Report',
            'class': 'bug-btn normal'
        },
        'ai': {
            'url': 'https://bugwise.shaktilab.org/research',
            'text': 'File Bug Report with AI',
            'class': 'bug-btn ai'
        }
    }
    # Define the order explicitly for indexing
    condition_keys_ordered = ['normal', 'ai']

    # Check if a valid condition is already assigned in the session
    assigned_condition_key = request.session.get('bug_report_condition')

    if assigned_condition_key not in BUG_REPORT_CONDITIONS:
        # Ensure the session has a key. This might create/save the session if it's new.
        if not request.session.session_key:
            request.session.create()

        # Use a more explicit 50-50 split method
        # Option 1: Random selection
        assigned_condition_key = random.choice(condition_keys_ordered)

        # Alternative Option 2: Session-based hash method (previous approach)
        # session_key = request.session.session_key
        # assignment_index = hash(session_key) % 2
        # assigned_condition_key = condition_keys_ordered[assignment_index]

        # Store the assigned condition in the session for persistence
        request.session['bug_report_condition'] = assigned_condition_key
        
        # Optional: Add logging or print for tracking
        print(f"User session {request.session.session_key}: Assigned bug report condition '{assigned_condition_key}'.")

    # Retrieve the details for the assigned condition
    assigned_condition_details = BUG_REPORT_CONDITIONS[assigned_condition_key]

    # Prepare button details for the template including tracking parameter
    button_url_with_tracking = f"{assigned_condition_details['url']}?condition={assigned_condition_key}"

    button_context = {
        'bug_report_url': button_url_with_tracking,
        'bug_report_text': assigned_condition_details['text'],
        'bug_report_class': assigned_condition_details['class'],
        'bug_report_condition': assigned_condition_key
    }

    # Fetch Todos (your existing logic)
    try:
        # Assuming Todo model exists and is imported
        todos = Todo.objects.all().order_by('-created_at')
    except NameError:
         # Handle case where Todo model might not be defined/imported
         print("Warning: Todo model not found or imported. Skipping Todo fetching.")
         todos = []

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