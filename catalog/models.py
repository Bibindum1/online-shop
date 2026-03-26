from django.db import models
from django.utils.text import slugify


def product_image_upload_path(instance, filename):
    slug = instance.slug if instance.slug else slugify(instance.name)
    return f'products/{slug}/{filename}'


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    position = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['position', 'name']
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

                self.slug = slug

            super().save(*args, **kwargs)

    def can_delete(self):
        return not self.products.exists()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)


    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.PROTECT
)

    slug = models.SlugField(max_length=255, unique=True, blank=True)

    description = models.TextField(blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)

    image = models.ImageField(
        upload_to=product_image_upload_path,
        blank=True,
        null=True
)

    position = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['position', 'name']


    verbose_name = "Товар"
    verbose_name_plural = "Товары"


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


    def __str__(self):
        return self.name


class ProductGallery(models.Model):


    product = models.ForeignKey(
        Product,
        related_name="gallery",
        on_delete=models.CASCADE
)

    image = models.ImageField(upload_to="products/gallery/")

    alt_text = models.CharField(max_length=200, blank=True)

    is_main = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["created_at"]


    def __str__(self):
        return f"Изображение {self.product.name}"
