#!/usr/bin/python3
#
# Part of RedELK
#
# Author: Lorenzo Bernardi / @fastlorenzo
#
from modules.helpers import *
import traceback
import config

info = {
    'version': 0.1,
    'name': 'dummy_alarm module',
    'alarmmsg': 'ALARM GENERATED BY LASTLINE',
    'description': 'This alarm always triggers. It lists the last 2 haproxy lines as hit',
    'type': 'redelk_alarm-NOTINUSE',
    'submodule': 'alarm_dummy'
}

class Module():
    def __init__(self):
        #print("class init")
        pass

    def run(self):
        ret = initial_alarm_result
        ret['info'] = info
        ret['fields'] = ['source.ip', 'source.nat.ip', 'source.geo.country_name', 'source.as.organization.name', 'redir.frontend.name', 'redir.backend.name', 'infra.attack_scenario', 'tags', 'redir.timestamp']
        ret['groupby'] = ['source.ip']
        try:
            report = self.alarm_check1()
            ret['hits']['hits'] = report['hits']
            ret['mutations'] = report['mutations'] # for this alarm this is an empty list
            ret['hits']['total'] = len(report['hits'])
        except Exception as e:
            stackTrace = traceback.format_exc()
            ret['error'] = stackTrace
            self.logger.exception(e)
            pass
        self.logger.info('finished running module. result: %s hits' % ret['hits']['total'])
        return(ret)

    def alarm_check(self):
        # This check queries for IP's that aren't listed in any iplist* but do talk to c2* paths on redirectors\n
        q = "*"
        i = countQuery(q)
        if i >= 10000:
            i = 10000
        r = getQuery(q, i)
        report = {}
        report['hits'] = []
        report['hits'].append(r[0])
        report['hits'].append(r[1])
        report['mutations'] = {}
        return(report)