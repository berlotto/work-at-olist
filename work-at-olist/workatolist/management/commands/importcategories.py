from django.core.management.base import BaseCommand
from django.utils.text import slugify

from workatolist.models import Channel, Category


class Command(BaseCommand):
    help = 'Import the channel categories and your subcategories'

    def add_arguments(self, parser):
        parser.add_argument('channel', type=str)
        parser.add_argument('filename', type=str)

    def check_category_slug_avaliability(self, slug):
        """
        Check if the slug text already exists in the database.
        If exists will append "-1", "-2", "-3", until it not exists,
        and return.
        """
        slug_text = slug
        counter = 1
        while Category.objects.filter(slug=slug_text).exists():
            slug_text = "{0}-{1}".format(slug, str(counter))
            counter += 1
        return slug_text

    def handle(self, *args, **options):
        channel_name = options['channel']
        file_name = options['filename']

        # Catch and remove all items of this channel
        channel, created = Channel.objects.get_or_create(
            slug=channel_name, name=channel_name)
        Category.objects.filter(channel=channel).delete()

        # Read the file and insert all new channel items
        count = 0
        with open(file_name, 'r') as file:
            for line in file.readlines():
                line_items = line.split("/")
                parent_obj = None  # Save the parent item to set in childs
                for item in line_items:  # Navigate in itens of line
                    category_name = item.strip()
                    if category_name:
                        cat = Category.objects.filter(
                            name=category_name,
                            channel=channel,
                            parent=parent_obj).first()
                        if not cat:
                            category_slug = self.check_category_slug_avaliability(
                                slugify(category_name))
                            cat = Category(
                                name=category_name,
                                slug=category_slug,
                                parent=parent_obj,
                                channel=channel,
                            )
                            cat.save()
                            count += 1
                        parent_obj = cat

        self.stdout.write(
            self.style.SUCCESS(
                ('Successfully imported {0} '
                 'categories for channel \'{1}\'').format(
                    count, channel_name)))
