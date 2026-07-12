from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Project, ProjectMember
from .forms import ProjectForm, AddMemberForm


@login_required
def dashboard(request):
    """Main dashboard showing all projects the user is part of."""
    # Projects the user owns
    owned_projects = Project.objects.filter(owner=request.user)

    # Projects the user is a member of (not owner)
    member_project_ids = ProjectMember.objects.filter(
        user=request.user
    ).values_list('project_id', flat=True)
    member_projects = Project.objects.filter(id__in=member_project_ids)

    # Combine both lists
    all_projects = (owned_projects | member_projects).distinct()

    context = {
        'projects': all_projects,
        'owned_count': owned_projects.count(),
    }
    return render(request, 'projects/dashboard.html', context)


@login_required
def project_create(request):
    """Create a new project."""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user  # Assign current user as owner
            project.save()
            messages.success(request, f'Project "{project.name}" created successfully!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()

    return render(request, 'projects/project_form.html', {'form': form, 'action': 'Create'})


@login_required
def project_detail(request, pk):
    """Show the Kanban board for a project."""
    project = get_object_or_404(Project, pk=pk)

    # Check if user has access to this project
    is_owner = project.owner == request.user
    is_member = ProjectMember.objects.filter(project=project, user=request.user).exists()

    if not is_owner and not is_member:
        messages.error(request, "You don't have access to this project.")
        return redirect('dashboard')

    # Get tasks grouped by status
    todo_tasks = project.tasks.filter(status='todo').order_by('-created_at')
    inprogress_tasks = project.tasks.filter(status='inprogress').order_by('-created_at')
    done_tasks = project.tasks.filter(status='done').order_by('-created_at')

    # Get all project members for task assignment
    members = ProjectMember.objects.filter(project=project).select_related('user')

    context = {
        'project': project,
        'is_owner': is_owner,
        'todo_tasks': todo_tasks,
        'inprogress_tasks': inprogress_tasks,
        'done_tasks': done_tasks,
        'members': members,
    }
    return render(request, 'projects/project_detail.html', context)


@login_required
def project_edit(request, pk):
    """Edit a project's details."""
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/project_form.html', {
        'form': form,
        'project': project,
        'action': 'Edit'
    })


@login_required
def project_delete(request, pk):
    """Delete a project (only owner can do this)."""
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    if request.method == 'POST':
        project_name = project.name
        project.delete()
        messages.success(request, f'Project "{project_name}" has been deleted.')
        return redirect('dashboard')

    return render(request, 'projects/project_confirm_delete.html', {'project': project})


@login_required
def manage_members(request, pk):
    """Add or remove members from a project."""
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    members = ProjectMember.objects.filter(project=project).select_related('user')

    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            role = form.cleaned_data['role']
            user = User.objects.get(username=username)

            # Don't add the owner as a member
            if user == project.owner:
                messages.warning(request, 'The project owner is already part of this project.')
            elif ProjectMember.objects.filter(project=project, user=user).exists():
                messages.warning(request, f'{username} is already a member.')
            else:
                ProjectMember.objects.create(project=project, user=user, role=role)
                messages.success(request, f'{username} added to the project!')
                return redirect('manage_members', pk=pk)
    else:
        form = AddMemberForm()

    return render(request, 'projects/members.html', {
        'project': project,
        'members': members,
        'form': form,
    })


@login_required
def remove_member(request, pk, user_id):
    """Remove a member from a project."""
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    member = get_object_or_404(ProjectMember, project=project, user_id=user_id)
    member.delete()
    messages.success(request, f'{member.user.username} removed from the project.')
    return redirect('manage_members', pk=pk)
