# -*- coding: utf-8 -*-

import datapackage_validate
import json
import os
from nose.tools import nottest

import unittest


class TestValidDatapackage(unittest.TestCase):

    @nottest
    def find_datapackage_files(self):
        for root, dirs, files in os.walk('.'):
            for filename in files:
                if filename == "datapackage.json":
                    yield (root, filename)

    def test_datapackage_json_validates(self):
        for root, filename in self.find_datapackage_files():
            with open(os.path.join(root, filename)) as f:
                datapackagejson = json.load(f)
                datapackage_validate.validate(datapackagejson)

    def test_datapackage_has_data_files(self):
        for root, filename in self.find_datapackage_files():
            with open(os.path.join(root, filename)) as f:
                datapackagejson = json.load(f)
                resources = datapackagejson["resources"]
                for resource in resources:
                    assert(os.path.isfile(os.path.join(root, resource["path"])))



