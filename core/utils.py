# import random 
# import string

# from django.utils.text import *

# def random_string_generator(size = 13, chars = string.ascii_lowercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))

# def unique_wed_matricule(instance):
#     new_wed_matricule = random_string_generator().upper()
    
#     klass = instance.__class__
#     qs_exists = klass.objects.filter(wed_matricule = new_wed_matricule).exists()
#     if qs_exists:
#         return unique_slug_generator(instance)
#     return new_wed_matricule

# def unique_divorse_matricule(instance):
#     new_divorse_matricule = random_string_generator().upper()
    
#     klass = instance.__class__
#     qs_exists = klass.objects.filter(divorse_matricule = new_divorse_matricule).exists()
#     if qs_exists:
#         return unique_slug_generator(instance)
#     return new_divorse_matricule

# def unique_slug_generator(instance, new_slug=None):
#     if new_slug is not None:
#         slug = new_slug
#     else:
#         slug = slugify(instance.title)
    
#     klass = instance.__class__
#     qs_exists = klass.objects.filter(slug=slug).exists()
#     if qs_exists:
#         new_slug = "{slug}-{randstr}".format(slug=slug, randstr=random_string_generator(size=13))
#         return unique_slug_generator(instance, new_slug=new_slug)
#     return slug