from django.core.management.base import BaseCommand

from bidnamic.ad_groups.tasks import get_ad_groups


class Command(BaseCommand):
    help = 'Gets or updates ad groups.'

    def add_arguments(self, parser):
        parser.add_argument('--chunk_size', type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Started.\nThis may take time, '
                                            'please be patient'))
        chunk_size = options.get('chunk_size') or 2000
        get_ad_groups(chunk_size=chunk_size)
        self.stdout.write(self.style.SUCCESS('Finished Successfully'))
