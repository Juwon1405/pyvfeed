#!/usr/bin/env python3
# API Python wrapper for The Vulnerability & Threat Intelligence Feed Service
# Copyright (C) 2013 - 2022 vFeed, Inc. - https://vfeed.io

import json

from lib.Database import Database
from common import utils as utility


class Risk(object):
    def __init__(self, id):
        """ init """
        self.id = id
        (self.cur, self.query) = Database(self.id).db_init()

    def get_kev_cisa(self):
        """ callable method - return CISA KEV Catalog"""
        # init
        response = {}

        # getting cvss data
        self.cur.execute('SELECT * FROM kev_cisa_db WHERE cve_id=?', self.query)
        self.datas = self.cur.fetchall()

        for data in self.datas:
            # setting cvss2 vectors
            self.kev_id = data[0]
            self.date_added = data[1]
            self.date_due = data[2]
            self.vuln_name = data[3]
            self.vendor = data[4]
            self.product = data[5]
            self.action = data[6]
            self.url = data[7]

            # format the response
            response = {"id": self.kev_id,
                        "parameters": {"date_added": self.date_added, "date_due": self.date_due,
                                       "name": self.vuln_name, "vendor": self.vendor,
                                       "product": self.product, "required_action": self.action,
                                       "url": self.url}}

        # adding the appropriate tag.
        response = {"kev": response}

        return utility.serialize_data(response)

    def get_epss(self):
        """ callable method - return EPSS scoring"""
        # init
        response = {}

        # getting cvss data
        self.cur.execute('SELECT * FROM epss_scoring WHERE cve_id=?', self.query)
        self.datas = self.cur.fetchall()

        for data in self.datas:
            # setting cvss2 vectors
            self.epss_probability = data[0]
            self.percentile_rank = data[1]

            response = {"probability": self.epss_probability, "percentile": self.percentile_rank}

        # adding the appropriate tag.
        response = {"epss": response}

        return utility.serialize_data(response)

    def get_cvss2(self):
        """ callable method - return  CVSS 2 score"""

        # init
        response = {}

        # getting cvss data
        self.cur.execute('SELECT * FROM cvss_scores WHERE cve_id=?', self.query)
        self.datas = self.cur.fetchall()

        for data in self.datas:
            # setting cvss2 vectors
            self.cvss2_base = data[0]
            self.cvss2_impact = data[1]
            self.cvss2_exploit = data[2]
            self.cvss2_vector = data[3]
            self.cvss2_access_vector = data[4]
            self.cvss2_access_complexity = data[5]
            self.cvss2_authentication = data[6]
            self.cvss2_conf_impact = data[7]
            self.cvss2_int_impact = data[8]
            self.cvss2_avail_impact = data[9]

            # formatting the response
            response = {"vector": self.cvss2_vector, "base_score": self.cvss2_base,
                        "impact_score": self.cvss2_impact,
                        "exploit_score": self.cvss2_exploit, "access_vector": self.cvss2_access_vector,
                        "access_complexity": self.cvss2_access_complexity,
                        "authentication": self.cvss2_authentication,
                        "confidentiality_impact": self.cvss2_conf_impact,
                        "integrity_impact": self.cvss2_int_impact, "availability_impact": self.cvss2_avail_impact}

        # adding the appropriate tag.
        response = {"cvss2": response}

        return utility.serialize_data(response)

    def get_cvss3(self):
        """ callable method - return CVSS 3 score"""

        # init
        response = {}

        # getting cvss data
        self.cur.execute('SELECT * FROM cvss_scores WHERE cve_id=?', self.query)
        self.datas = self.cur.fetchall()

        for data in self.datas:
            # setting cvss3 vectors
            self.cvss3_base = data[10]
            self.cvss3_impact = data[11]
            self.cvss3_exploit = data[12]
            self.cvss3_vector = data[13]
            self.cvss3_attack_vector = data[14]
            self.cvss3_attack_complexity = data[15]
            self.cvss3_privileges_required = data[16]
            self.cvss3_user_interaction = data[17]
            self.cvss3_scope = data[18]
            self.cvss3_conf_impact = data[19]
            self.cvss3_int_impact = data[20]
            self.cvss3_avail_impact = data[21]

            # formatting the response
            response = {"vector": self.cvss3_vector, "base_score": self.cvss3_base,
                        "impact_score": self.cvss3_impact,
                        "exploit_score": self.cvss3_exploit, "attack_vector": self.cvss3_attack_vector,
                        "attack_complexity": self.cvss3_attack_complexity,
                        "privileges_required": self.cvss3_privileges_required,
                        "user_interaction": self.cvss3_user_interaction, "score": self.cvss3_scope,
                        "confidentiality_impact": self.cvss3_conf_impact,
                        "integrity_impact": self.cvss3_int_impact, "availability_impact": self.cvss3_avail_impact}

        # adding the appropriate tag.
        response = {"cvss3": response}

        return utility.serialize_data(response)

    def get_cvss(self):
        """ callable method - return both CVSS 2 and 3 scores"""

        cvss_2 = json.loads(self.get_cvss2())
        cvss_3 = json.loads(self.get_cvss3())
        cvss_2.update(cvss_3)

        # formatting the response
        response = {"cvss": cvss_2}

        return utility.serialize_data(response)

    def get_risk(self):
        """ callable method - return all risks"""
        response = json.loads(Risk(self.id).get_cvss())
        epss = json.loads(Risk(self.id).get_epss())
        kev_cisa = json.loads(Risk(self.id).get_kev_cisa())

        # formatting the response
        response.update(epss)
        response.update(kev_cisa)
        response = {"risk": response}

        return utility.serialize_data(response)
