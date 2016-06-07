from django.core.management.base import BaseCommand
from remanage.models import User, Property
from mongoengine import *
from realup.settings import MONGO_DB
import json
import os

connect(MONGO_DB)


class Command(BaseCommand):
    help = 'Populate the development database with seed data'

    @staticmethod
    def get_data(filename):
        with open(filename) as f:
            data = json.load(f)
        return data

    def add_arguments(self, parser):
        parser.add_argument('-c', '--clear', action='store_true', default=False, dest='clear',
                            help='clear existing data from collections')

    def handle(self, *args, **options):
        clear = options['clear']

        if clear:
            User.objects().delete({})
            Property.objects().delete({})

        directory = os.path.dirname(__file__)
        users_data = self.get_data(os.path.join(directory, 'users_seed_data.json'))
        users = []
        for user_data in users_data:
            my_user = User(**user_data)
            my_user.save()
            users.append(my_user)

        properties_data = self.get_data(os.path.join(directory, 'properties_seed_data.json'))
        i = 0
        for property_data in properties_data:
            property_data['user'] = users[i]
            my_property = Property(**property_data)
            i = 0 if i >= len(users) else i + 1
            my_property.save()