#!/usr/bin/env python
# -*- coding: utf-8 -*-

import users as models

import datetime

class GameBrain(object):
    

    def commands(cls):
        d =dict()
        ret_async = models.Commands.get_list_async()
        for res in ret_async.get_result():
            d[res.key.urlsafe()] = cls.to_dict(res)

        return d


    def matches(cls):

        l = []

        ret_async = models.Matches.get_list_async()
        for res  in ret_async.get_result():

            l.append(cls.to_dict(res))

        return l

    def user_rates(cls):

        d = {}

        ret_async = models.UserRates.get_list_async()
        for res  in ret_async.get_result():
            d[res.user.urlsafe()+"_"+res.match.urlsafe()] = cls.to_dict_dict(res.to_dict())
        return d

    def users(cls):

        d = {}

        ret_async = models.Users.get_list_async()
        for res  in ret_async.get_result():
            d[res.key.urlsafe()] = cls.to_dict_dict(res.to_dict())
            
        return d

    def coerce(cls, value):
        SIMPLE_TYPES = (int, long, float, bool, basestring,)
        if value is None or isinstance(value, SIMPLE_TYPES):
            return value
        elif isinstance(value, datetime.date):
            return value.isoformat()
        elif hasattr(value, 'to_dict'):    # hooray for duck typing!
            return value.to_dict()
        elif isinstance(value, dict):
            return dict((coerce(k), coerce(v)) for (k, v) in value.items())
        elif hasattr(value, '__iter__'):    # iterable, not string
            return map(coerce, value)
        else:
            return value.urlsafe()


    def to_dict(cls, model):
        output = {}
        for key, prop in model._properties.iteritems():
            value = cls.coerce(getattr(model, key))
            if value is not None:
                output[key] = value

        return output

    def to_dict_dict(cls, from_dict):
        output = {}
        for key, prop in from_dict.items():
            value = cls.coerce(prop)
            if value is not None:
                output[key] = value

        return output        
