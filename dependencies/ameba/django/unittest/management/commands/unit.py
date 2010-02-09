import os
import unittest
 
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) > 0:
            self.test_case = args[0]
        self.handle_noargs(**options)
        
    def handle_noargs(self, **options):
        self.project_name = os.path.basename(settings.PROJECT_PATH)
        self.unittests_path = os.path.join(settings.PROJECT_PATH, 'tests', 'unittests')
        unittest.TextTestRunner(verbosity=1).run(self.get_suite())

    def get_suite(self):
        modules = []
        for root, _, files in os.walk(self.unittests_path):
            if not files: continue
            for file in files:
                if not (file.startswith('test_') and file.endswith('.py')): continue     
                path = '%s.%s' % (root.replace(self.unittests_path, '').replace('/', '.'), file)
                module = self.project_name + '.tests.unittests.' + path[1:].replace('.py', '')
                
                if hasattr(self, 'test_case'):
                    if file == 'test_' + self.test_case + '.py':
                        modules.append(__import__(module, fromlist=['*']))
                        break
                else:
                    modules.append(__import__(module, fromlist=['*']))
        
        load = unittest.defaultTestLoader.loadTestsFromModule
        return unittest.TestSuite(map(load, modules))
