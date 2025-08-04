from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import get_language
from django.conf import settings

from parler.utils.context import switch_language
from parler.models import TranslatableModel


def get_blog_languages():
    from .models import Post
    return Post.objects.exclude(language__isnull=True).order_by('language').values_list(
        'language', flat=True).distinct()


def get_blog_authors(coauthors=True):
    now = timezone.now()

    filters = (
        (Q(post__publication_end__isnull=True) | Q(post__publication_end__gte=now))
        & (Q(post__language=get_language()) | Q(post__language__isnull=True))
        & Q(post__publication_start__lte=now)
    )

    if coauthors:
        coauthors_filters = (
            (Q(aldryn_blog_coauthors__publication_end__isnull=True) |
             Q(aldryn_blog_coauthors__publication_end__gte=now))
            & (Q(aldryn_blog_coauthors__language=get_language()) | Q(aldryn_blog_coauthors__language__isnull=True))
            & Q(aldryn_blog_coauthors__publication_start__lte=now)
        )

        filters = (filters | coauthors_filters)

    return User.objects.filter(filters).distinct()


def generate_slugs(users):
    """
    Takes a queryset of users and creates nice slugs
    Returns the same queryset but with a slug attribute on each user
    """

    slugs = []
    slugged_users = []

    for user in users:
        slug = ''
        _slug = slugify(user.get_full_name())
        if not _slug:
            slug = user.get_username()

        elif _slug not in slugs:
            slug = _slug

        else:
            for i in range(2, 100):
                if not '%s-%i' % (_slug, i) in slugs:
                    slug = '%s-%i' % (_slug, i)
                    break

        if not slug:
            slug = user.get_username()

        slugs.append(slug)
        user.slug = slug
        slugged_users.append(user)

    return slugged_users


def get_user_from_slug(find_slug):
    authors = generate_slugs(get_blog_authors())
    for author in authors:
        if author.slug == find_slug:
            return author
    return None


def get_slug_for_user(find_user):
    authors = generate_slugs(get_blog_authors())
    for author in authors:
        if author == find_user:
            return author.slug


def get_slug_in_language(record, language):
    if not record or not isinstance(record, TranslatableModel):
        return None

    # Try to get translation in the requested language
    try:
        with switch_language(record, language):
            return record.slug
    except (AttributeError, ObjectDoesNotExist):
        return None


def paginate_by(fallback=None):
    try:
        return settings.ALDRYN_BLOG_PAGINATOR_PAGINATE_BY
    except AttributeError:
        return fallback or 5