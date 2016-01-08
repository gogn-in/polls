# -*- coding: utf-8 -*-

import datapackage_validate
import json
import os
import unittest


class TestValidDatapackage(unittest.TestCase):

    def test_datapackage(self):
        for root, dirs, files in os.walk('.'):
            for filename in files:
                if filename == "datapackage.json":
                    f = open(os.path.join(root, filename))
                    datapackagejson = json.load(f)
                    datapackage_validate.validate(datapackagejson)


