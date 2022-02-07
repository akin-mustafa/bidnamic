from django.core.management.base import BaseCommand, CommandError

from bidnamic.search_terms.tasks import get_all


class Command(BaseCommand):
    help = 'Gets or updates search terms.'

    def add_arguments(self, parser):
        parser.add_argument('--chunk_size', type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Started.\nThis will take time, '
                                            'please be patient'))
        chunk_size = options.get('chunk_size') or 2000
        get_all(chunk_size)
        self.stdout.write(self.style.SUCCESS('Finished Successfully'))
