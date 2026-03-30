from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Recipe


def home(request):
    featured_recipes = Recipe.objects.filter(is_published=True, is_featured=True)[:3]

    context = {
        'featured_recipes': featured_recipes,
    }

    return render(request, 'home.html', context)


def recipe_list(request):
    search = request.GET.get('search', '').strip()
    category = request.GET.get('category', '').strip()
    difficulty = request.GET.get('difficulty', '').strip()
    ordering = request.GET.get('ordering', '').strip()

    recipes = Recipe.objects.filter(is_published=True)

    if search:
        recipes = recipes.filter(
            Q(title__icontains=search) |
            Q(short_description__icontains=search)
        )

    if category:
        recipes = recipes.filter(category=category)

    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)

    ordering_map = {
        'title_asc': 'title',
        'title_desc': '-title',
        'created_desc': '-created_at',
        'created_asc': 'created_at',
        'prep_time_asc': 'prep_time',
        'prep_time_desc': '-prep_time',
    }

    if ordering in ordering_map:
        recipes = recipes.order_by(ordering_map[ordering])
    else:
        recipes = recipes.order_by('-created_at')

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'recipes': page_obj,
        'page_obj': page_obj,
        'search': search,
        'selected_category': category,
        'selected_difficulty': difficulty,
        'selected_ordering': ordering,
        'category_choices': Recipe.CategoryChoices.choices,
        'difficulty_choices': Recipe.DifficultyChoices.choices,
    }

    return render(request, 'recipes/recipe_list.html', context)


def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, is_published=True)

    context = {
        'recipe': recipe,
    }

    return render(request, 'recipes/recipe_detail.html', context)


def dashboard(request):
    total_recipes = Recipe.objects.count()
    published_recipes = Recipe.objects.filter(is_published=True).count()
    draft_recipes = Recipe.objects.filter(is_published=False).count()
    featured_recipes_count = Recipe.objects.filter(is_featured=True).count()

    latest_recipes = Recipe.objects.order_by('-created_at')[:5]

    recipes_by_category = (
        Recipe.objects
        .values('category')
        .annotate(total=Count('id'))
        .order_by('-total', 'category')
    )

    context = {
        'total_recipes': total_recipes,
        'published_recipes': published_recipes,
        'draft_recipes': draft_recipes,
        'featured_recipes_count': featured_recipes_count,
        'latest_recipes': latest_recipes,
        'recipes_by_category': recipes_by_category,
        'category_labels': dict(Recipe.CategoryChoices.choices),
    }

    return render(request, 'recipes/dashboard.html', context)


def dashboard_recipe_list(request):
    search = request.GET.get('search', '').strip()
    category = request.GET.get('category', '').strip()
    difficulty = request.GET.get('difficulty', '').strip()
    publication_status = request.GET.get('publication_status', '').strip()
    ordering = request.GET.get('ordering', '').strip()

    recipes = Recipe.objects.all()

    if search:
        recipes = recipes.filter(
            Q(title__icontains=search) |
            Q(short_description__icontains=search)
        )

    if category:
        recipes = recipes.filter(category=category)

    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)

    if publication_status == 'published':
        recipes = recipes.filter(is_published=True)
    elif publication_status == 'draft':
        recipes = recipes.filter(is_published=False)

    ordering_map = {
        'title_asc': 'title',
        'title_desc': '-title',
        'created_desc': '-created_at',
        'created_asc': 'created_at',
        'prep_time_asc': 'prep_time',
        'prep_time_desc': '-prep_time',
    }

    if ordering in ordering_map:
        recipes = recipes.order_by(ordering_map[ordering])
    else:
        recipes = recipes.order_by('-created_at')

    paginator = Paginator(recipes, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'recipes': page_obj,
        'page_obj': page_obj,
        'search': search,
        'selected_category': category,
        'selected_difficulty': difficulty,
        'selected_publication_status': publication_status,
        'selected_ordering': ordering,
        'category_choices': Recipe.CategoryChoices.choices,
        'difficulty_choices': Recipe.DifficultyChoices.choices,
    }

    return render(request, 'recipes/dashboard_recipe_list.html', context)

def dashboard_recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    context = {
        'recipe': recipe,
    }

    return render(request, 'recipes/dashboard_recipe_detail.html', context)

def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save()
            messages.success(
                request,
                f'La ricetta "{recipe.title}" è stata creata con successo.'
            )
            return redirect('dashboard_recipe_list')
        messages.error(
            request,
            'Impossibile creare la ricetta. Controlla i campi evidenziati.'
        )
    else:
        form = RecipeForm()

    context = {
        'form': form,
        'page_title': 'Nuova ricetta',
        'submit_label': 'Crea ricetta',
    }

    return render(request, 'recipes/recipe_form.html', context)


def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save()
            messages.success(
                request,
                f'La ricetta "{recipe.title}" è stata aggiornata correttamente.'
            )
            return redirect('dashboard_recipe_list')
        messages.error(
            request,
            'Impossibile aggiornare la ricetta. Controlla i campi evidenziati.'
        )
    else:
        form = RecipeForm(instance=recipe)

    context = {
        'form': form,
        'recipe': recipe,
        'page_title': 'Modifica ricetta',
        'submit_label': 'Salva modifiche',
    }

    return render(request, 'recipes/recipe_form.html', context)


def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        recipe_title = recipe.title
        recipe.delete()
        messages.success(
            request,
            f'La ricetta "{recipe_title}" è stata eliminata con successo.'
        )
        return redirect('dashboard_recipe_list')

    context = {
        'recipe': recipe,
    }

    return render(request, 'recipes/recipe_confirm_delete.html', context)