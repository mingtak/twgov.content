import doctest
import unittest

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

import twgov.content

OPTION_FLAGS = doctest.NORMALIZE_WHITESPACE | \
               doctest.ELLIPSIS

ptc.setupPloneSite(products=['twgov.content'])


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            zcml.load_config('configure.zcml',
              twgov.content)

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='twgov.content',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='twgov.content.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'INTEGRATION.txt',
            package='twgov.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),

        # -*- extra stuff goes here -*-

        # Integration tests for NewRelationNotice
        ztc.ZopeDocFileSuite(
            'NewRelationNotice.txt',
            package='twgov.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for RelationNotice
        ztc.ZopeDocFileSuite(
            'RelationNotice.txt',
            package='twgov.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for SpecialViews
        ztc.ZopeDocFileSuite(
            'SpecialViews.txt',
            package='twgov.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for profileSetting
        ztc.ZopeDocFileSuite(
            'profileSetting.txt',
            package='twgov.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for govNotice
        ztc.ZopeDocFileSuite(
            'govNotice.txt',
            package='twgov.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
