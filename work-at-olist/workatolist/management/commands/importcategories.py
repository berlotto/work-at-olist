from django.core.management.base import BaseCommand
from django.utils.text import slugify

from workatolist.models import Channel, Category


class Command(BaseCommand):
    help = 'Import the channel categories and your subcategories'

    def add_arguments(self, parser):
        parser.add_argument('channel', type=str)
        parser.add_argument('filename', type=str)

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
                        c = Category.objects.filter(
                            name=category_name,
                            channel=channel).first()
                        if not c:
                            c = Category(
                                name=category_name,
                                slug=slugify(category_name),
                                parent=parent_obj,
                                channel=channel,
                            )
                            c.save()
                            count += 1
                        parent_obj = c

        self.stdout.write(
            self.style.SUCCESS(
                ('Successfully imported {0} '
                 'categories for channel \'{1}\'').format(
                    count, channel_name)))
