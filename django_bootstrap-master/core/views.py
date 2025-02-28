from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Todo
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'index.html', {})
def examples(request):
    return render(request, 'examp.html', {})
def team(request):
    return render(request, 'team.html', {})
def home(request):
    todos = Todo.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'todos': todos})

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