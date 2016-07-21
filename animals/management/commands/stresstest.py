from django.core.management.base import (
    BaseCommand,
    CommandError
)

from animals.models import Animal


class Command(BaseCommand):
    help = 'Create the conditions for a stress test for any front-end app consuming the API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=1000,
            help='The number of animals to insert',
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            dest='reset',
            default=False,
            help='Remove all animals',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Deleting all animals...')
            self.stdout.write(self.style.SUCCESS('Successfull delete : {}'.format(Animal.objects.all().delete())))
        else:
            Animal.objects.bulk_create([Animal(name='animal_{}'.format(i)) for i in range(options['total'])])
            self.stdout.write(self.style.SUCCESS('Successfully added {} animals'.format(options['total'])))
