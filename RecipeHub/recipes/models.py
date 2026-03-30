from django.db import models

# Create your models here.

from django.db import models
from django.utils.text import slugify


class Recipe(models.Model):
    class DifficultyChoices(models.TextChoices):
        EASY = 'easy', 'Facile'
        MEDIUM = 'medium', 'Media'
        HARD = 'hard', 'Difficile'
        EXPERT = "expert", 'Esperta'

    class CategoryChoices(models.TextChoices):
        APPETIZER = 'appetizer', 'Antipasto'
        FIRST_COURSE = 'first_course', 'Primo'
        SECOND_COURSE = 'second_course', 'Secondo'
        SIDE_DISH = 'side_dish', 'Contorno'
        DESSERT = 'dessert', 'Dolce'
        OTHER = 'other', 'Altro'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.TextField(blank=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    prep_time = models.PositiveIntegerField(help_text='Tempo di preparazione in minuti')
    cook_time = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='Tempo di cottura in minuti'
    )
    servings = models.PositiveIntegerField(blank=True, null=True)
    difficulty = models.CharField(
        max_length=20,
        choices=DifficultyChoices.choices,
        default=DifficultyChoices.EASY
    )
    category = models.CharField(
        max_length=30,
        choices=CategoryChoices.choices,
        default=CategoryChoices.OTHER
    )
    cuisine_type = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ricetta'
        verbose_name_plural = 'Ricette'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Recipe.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    @property
    def total_time(self):
        return self.prep_time + (self.cook_time or 0)