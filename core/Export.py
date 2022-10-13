#!/usr/bin/env python3
# API Python wrapper for The Vulnerability & Threat Intelligence Feed Service
# Copyright (C) 2013 - 2022 vFeed, Inc. - https://vfeed.io

import json

from core.Risk import Risk
from core.Defense import Defense
from lib.Database import Database
from common import utils as utility
from core.Inspection import Inspection
from core.Information import Information
from core.Exploitation import Exploitation
from core.Classification import Classification


class Export(object):
    def __init__(self, id):
        """init """

        self.id = id
        (self.cur, self.query) = Database(self.id).db_init()
        self.json_file = str.join('.', (self.id.upper(), 'json'))
        self.yaml_file = str.join('.', (self.id.upper(), 'yaml'))

    def load_data(self):
        """ load metadata related to vuln"""

        # loading data
        response = json.loads(Information(self.id).get_all())
        classification = json.loads(Classification(self.id).get_all())
        risk = json.loads(Risk(self.id).get_risk())
        inspection = json.loads(Inspection(self.id).get_all())
        exploitation = json.loads(Exploitation(self.id).get_exploits())
        defense = json.loads(Defense(self.id).get_all())

        # formatting the response
        response.update(classification)
        response.update(risk)
        response.update(inspection)
        response.update(exploitation)
        response.update(defense)

        return response

    def dump_json(self):
        """ callable method - export to JSON  """

        # create json file
        utility.create_json(self.load_data(), self.json_file)

    def dump_yaml(self):
        """ callable method - export to YAML  """

        # create yaml file
        utility.create_yaml(self.load_data(), self.yaml_file)
