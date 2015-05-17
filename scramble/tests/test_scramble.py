import os
import shutil
import unittest

import pkg_resources

from scramble.command import main

SCRAMBLE_TMP = '/tmp/scramble_tests'


class ScrambleTestCase(unittest.TestCase):

    def setUp(self):
        self.start_dir = os.getcwd()
        super(ScrambleTestCase, self).setUp()
        os.makedirs(SCRAMBLE_TMP)
        os.chdir(SCRAMBLE_TMP)
        
    def tearDown(self):
        super(ScrambleTestCase, self).tearDown()
        os.chdir(self.start_dir)
        shutil.rmtree(SCRAMBLE_TMP)
        
    def test_scramble_command(self):
        main()
        self.assertEqual(
            os.listdir(SCRAMBLE_TMP), ['scrambled'])

        ws = pkg_resources.working_set

        expected = []
        for name, dist in ws.by_key.items(): 
            top_level = sorted(list(dist._get_metadata('top_level.txt')))
            expected += top_level
        expected = set(expected)

        linked = []
        for link in os.listdir(os.path.join(SCRAMBLE_TMP, 'scrambled')):
            if link.endswith(".py"):
                linked.append(link[:-3])
            else:
                linked.append(link)

        print(linked)
        print(expected) 
        self.assertEqual(
            sorted(linked),
            sorted(expected))

    def test_scramble_command_custom_dir(self):
        main(['--target', 'custom_scrambled'])
        self.assertEqual(
            os.listdir(SCRAMBLE_TMP), ['custom_scrambled'])

        ws = pkg_resources.working_set

        expected = []
        for name, dist in ws.by_key.items(): 
            top_level = sorted(list(dist._get_metadata('top_level.txt')))
            expected += top_level
        expected = set(expected)

        linked = []
        for link in os.listdir(os.path.join(SCRAMBLE_TMP, 'custom_scrambled')):
            if link.endswith(".py"):
                linked.append(link[:-3])
            else:
                linked.append(link)
        
        self.assertEqual(
            sorted(linked),
            sorted(expected))
        

    def test_scramble_command_namespaced(self):
        main()

        ws = pkg_resources.working_set        

        namespaces = {}
        for name, dist in ws.by_key.items():
            for line in dist._get_metadata('namespace_packages.txt'):
                ns = line.split('.')[0]
                if not ns in namespaces:
                    namespaces[ns] = []
                namespaces[ns].append(dist)

        for namespace, dists in namespaces.items():
            linked = sorted(
                [x for x in os.listdir(
                    os.path.join(SCRAMBLE_TMP, 'scrambled', namespace))
                 if os.path.isdir(os.path.join(SCRAMBLE_TMP, 'scrambled', namespace, x))
                 and not x.startswith('__')])

            expected = []
            for dist in dists:
                expected += [
                    x for x in os.listdir(os.path.join(dist.location, namespace))
                    if os.path.isdir(os.path.join(dist.location, namespace, x))
                    and not x.startswith("__")]

            expected = sorted(set(expected))

            self.assertEqual(linked, expected)
