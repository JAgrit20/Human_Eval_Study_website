from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Todo
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache  
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
def gp2(request):
    return render(request, 'gp2.html', {})

SURVEY_URLS = [
    "https://example.com/survey/1",
    "https://example.com/survey/2",
    "https://example.com/survey/3",
    "https://example.com/survey/4",
    "https://example.com/survey/5",
    "https://example.com/survey/6",
    "https://example.com/survey/7",
    "https://example.com/survey/8",
    "https://example.com/survey/9",
    "https://example.com/survey/10",
]

def start_survey(request):
    """
    Atomically increment a counter held in the cache and
    redirect to the next survey URL.
    """
    if request.method != "POST":
        return redirect("landing")   # defensive fallback

    # make sure the key exists, then bump it
    cache.add("survey_counter", 0)          # no‑op if it already exists
    click_no = cache.incr("survey_counter")  # returns 1, 2, 3, …

    target = SURVEY_URLS[(click_no - 1) % len(SURVEY_URLS)]
    return redirect(target)
import random
from django.shortcuts import render
def _get_session_key(request):
    """Ensures a session key exists and returns it."""
    if not request.session.session_key:
        request.session.create() # Create session if it doesn't exist
    return request.session.session_key


def home(request):
    session_key = _get_session_key(request)
    BUG_REPORT_CONDITIONS = {
        'normal': {
            'url': 'https://bugwise.shaktilab.org/report_it',
            'text': 'File Bug Report',
            'class': 'bug-btn normal'
        },
        'ai': {
            'url': 'https://bugwise.shaktilab.org/research',
            'text': 'File Bug Report',
            'class': 'bug-btn normal'
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
        todos = Todo.objects.filter(session_key=session_key).order_by('-created_at')
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
            session_key = _get_session_key(request)
            todo = Todo.objects.create(title=title, session_key=session_key)
            return JsonResponse({
                'id': todo.id,
                'title': todo.title,
                'completed': todo.completed,
                'created_at': todo.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
    return JsonResponse({'error': 'Invalid data'}, status=400)

@csrf_exempt
def toggle_todo(request, todo_id):
    if request.method == 'POST':
        session_key = _get_session_key(request)
        todo = get_object_or_404(Todo, id=todo_id, session_key=session_key)
        todo.completed = not todo.completed
        todo.save()
        return JsonResponse({
            'id': todo.id,
            'completed': todo.completed
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def delete_todo(request, todo_id):
    if request.method == 'POST':
        session_key = _get_session_key(request)
        # This line ensures only the item with the correct id AND belonging
        # to the current session can be fetched.
        todo = get_object_or_404(Todo, id=todo_id, session_key=session_key)
        todo.delete()
        return JsonResponse({'status': 'success'}) # <-- Sending 'status' key
    return JsonResponse({'error': 'Invalid request'}, status=400)