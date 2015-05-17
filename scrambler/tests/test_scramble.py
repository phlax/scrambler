import os
import shutil
import unittest

import pkg_resources

from scrambler.command import main

SCRAMBLER_TMP = '/tmp/scrambler_tests'


class ScramblerTestCase(unittest.TestCase):

    def setUp(self):
        self.start_dir = os.getcwd()
        super(ScramblerTestCase, self).setUp()
        os.makedirs(SCRAMBLER_TMP)
        os.chdir(SCRAMBLER_TMP)
        
    def tearDown(self):
        super(ScramblerTestCase, self).tearDown()
        os.chdir(self.start_dir)
        shutil.rmtree(SCRAMBLER_TMP)
        
    def test_scrambler_command(self):
        main()
        self.assertEqual(
            os.listdir(SCRAMBLER_TMP), ['scrambled'])

        ws = pkg_resources.working_set

        expected = []
        for name, dist in ws.by_key.items(): 
            top_level = sorted(list(dist._get_metadata('top_level.txt')))
            expected += top_level
        expected = set(expected)

        linked = []
        for link in os.listdir(os.path.join(SCRAMBLER_TMP, 'scrambled')):
            if link.endswith(".py"):
                linked.append(link[:-3])
            else:
                linked.append(link)

        self.assertEqual(
            sorted(linked),
            sorted(expected))

    def test_scrambler_command_custom_dir(self):
        main(['--target', 'custom_scrambled'])
        self.assertEqual(
            os.listdir(SCRAMBLER_TMP), ['custom_scrambled'])

        ws = pkg_resources.working_set

        expected = []
        for name, dist in ws.by_key.items(): 
            top_level = sorted(list(dist._get_metadata('top_level.txt')))
            expected += top_level
        expected = set(expected)

        linked = []
        for link in os.listdir(os.path.join(SCRAMBLER_TMP, 'custom_scrambled')):
            if link.endswith(".py"):
                linked.append(link[:-3])
            else:
                linked.append(link)
        
        self.assertEqual(
            sorted(linked),
            sorted(expected))
        

    def test_scrambler_command_namespaced(self):
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
                    os.path.join(SCRAMBLER_TMP, 'scrambled', namespace))
                 if os.path.isdir(os.path.join(SCRAMBLER_TMP, 'scrambled', namespace, x))
                 and not x.startswith('__')])

            expected = []
            for dist in dists:
                expected += [
                    x for x in os.listdir(os.path.join(dist.location, namespace))
                    if os.path.isdir(os.path.join(dist.location, namespace, x))
                    and not x.startswith("__")]

            expected = sorted(set(expected))
            self.assertEqual(linked, expected)
