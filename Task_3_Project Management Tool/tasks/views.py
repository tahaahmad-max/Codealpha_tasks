from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from projects.models import Project, ProjectMember
from .models import Task, Comment, Notification
from .forms import TaskForm, CommentForm


def can_access_project(user, project):
    """Check if a user can access a project (is owner or member)."""
    is_owner = project.owner == user
    is_member = ProjectMember.objects.filter(project=project, user=user).exists()
    return is_owner or is_member


def send_notification(recipient, message, task=None):
    """Create a notification for a user."""
    if recipient:
        Notification.objects.create(recipient=recipient, message=message, task=task)


@login_required
def task_create(request, project_pk):
    """Create a new task in a project."""
    project = get_object_or_404(Project, pk=project_pk)

    if not can_access_project(request.user, project):
        messages.error(request, "You don't have access to this project.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = TaskForm(project, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.save()

            # Notify assigned user (if different from creator)
            if task.assigned_to and task.assigned_to != request.user:
                send_notification(
                    recipient=task.assigned_to,
                    message=f'{request.user.get_full_name() or request.user.username} assigned you a task: "{task.title}" in project "{project.name}".',
                    task=task
                )

            messages.success(request, f'Task "{task.title}" created!')
            return redirect('project_detail', pk=project.pk)
    else:
        # Pre-select status if passed as query param (e.g., from a column button)
        initial_status = request.GET.get('status', 'todo')
        form = TaskForm(project, initial={'status': initial_status})

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'project': project,
        'action': 'Create'
    })


@login_required
def task_detail(request, pk):
    """Show task detail with comments."""
    task = get_object_or_404(Task, pk=pk)
    project = task.project

    if not can_access_project(request.user, project):
        messages.error(request, "You don't have access to this task.")
        return redirect('dashboard')

    comment_form = CommentForm()
    comments = task.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()

            # Notify task creator if someone else comments
            if task.created_by != request.user:
                send_notification(
                    recipient=task.created_by,
                    message=f'{request.user.get_full_name() or request.user.username} commented on your task: "{task.title}".',
                    task=task
                )
            # Also notify assigned user if different
            if task.assigned_to and task.assigned_to != request.user and task.assigned_to != task.created_by:
                send_notification(
                    recipient=task.assigned_to,
                    message=f'{request.user.get_full_name() or request.user.username} commented on task "{task.title}" assigned to you.',
                    task=task
                )

            messages.success(request, 'Comment added!')
            return redirect('task_detail', pk=task.pk)

    context = {
        'task': task,
        'project': project,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'tasks/task_detail.html', context)


@login_required
def task_edit(request, pk):
    """Edit an existing task."""
    task = get_object_or_404(Task, pk=pk)
    project = task.project

    if not can_access_project(request.user, project):
        messages.error(request, "You don't have access to this task.")
        return redirect('dashboard')

    old_assigned = task.assigned_to

    if request.method == 'POST':
        form = TaskForm(project, request.POST, instance=task)
        if form.is_valid():
            task = form.save()

            # Notify new assignee if assignment changed
            new_assigned = task.assigned_to
            if new_assigned and new_assigned != old_assigned and new_assigned != request.user:
                send_notification(
                    recipient=new_assigned,
                    message=f'{request.user.get_full_name() or request.user.username} assigned you a task: "{task.title}" in project "{project.name}".',
                    task=task
                )

            messages.success(request, 'Task updated successfully!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(project, instance=task)

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'task': task,
        'project': project,
        'action': 'Edit'
    })


@login_required
def task_delete(request, pk):
    """Delete a task."""
    task = get_object_or_404(Task, pk=pk)
    project = task.project

    # Only project owner or task creator can delete
    if not (project.owner == request.user or task.created_by == request.user):
        messages.error(request, "You don't have permission to delete this task.")
        return redirect('task_detail', pk=task.pk)

    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f'Task "{task_title}" deleted.')
        return redirect('project_detail', pk=project.pk)

    return render(request, 'tasks/task_confirm_delete.html', {
        'task': task,
        'project': project
    })


@login_required
def task_update_status(request, pk):
    """Quick-update task status (used by drag-and-drop or buttons)."""
    task = get_object_or_404(Task, pk=pk)
    project = task.project

    if not can_access_project(request.user, project):
        messages.error(request, "You don't have access.")
        return redirect('dashboard')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = ['todo', 'inprogress', 'done']
        if new_status in valid_statuses:
            task.status = new_status
            task.save()
            messages.success(request, f'Task moved to {task.get_status_display()}.')

    return redirect('project_detail', pk=project.pk)


@login_required
def delete_comment(request, pk):
    """Delete a comment (only the author can do this)."""
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    task_pk = comment.task.pk
    comment.delete()
    messages.success(request, 'Comment deleted.')
    return redirect('task_detail', pk=task_pk)


@login_required
def notifications(request):
    """Show all notifications for the current user."""
    user_notifications = Notification.objects.filter(recipient=request.user)

    # Mark all as read when viewing the page
    user_notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'tasks/notifications.html', {
        'notifications': user_notifications,
    })
