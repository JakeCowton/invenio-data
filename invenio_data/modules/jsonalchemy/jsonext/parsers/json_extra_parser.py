# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2013 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 60 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from pyparsing import Optional, Keyword, Literal

from invenio.base.utils import try_to_eval

from invenio.modules.jsonalchemy.registry import functions
from invenio.modules.jsonalchemy.parser import FieldBaseExtensionParser, \
    PYTHON_ALLOWED_EXPR, indentedBlock


class JsonExtraParser(FieldBaseExtensionParser):
    """
    Class to parse and store the information related with how to load and dump
    a non-json object.

    It parses something like this::

        json:
            loads, function_to_load(field)
            dumps, function_to_dump(field)

    The functions to load and dump must have one parameter which is the field
    to parse.
    """

    __parsername__ = 'json_ext'

    @classmethod
    def parse_element(cls, indent_stack):
        """Sets ``json_ext`` in the rule"""
        json_dumps = (Keyword('dumps').suppress() +
                      Literal(',').suppress() +
                      PYTHON_ALLOWED_EXPR)\
                     .setResultsName("dumps")\
                     .setParseAction(lambda toks: toks[0].strip())
        json_loads = (Keyword("loads").suppress() +
                      Literal(",").suppress() +
                      PYTHON_ALLOWED_EXPR)\
                     .setResultsName("loads")\
                     .setParseAction(lambda toks: toks[0].strip())
        return (Keyword('json:').suppress() +
                indentedBlock((json_dumps & json_loads), indent_stack)
               ).setResultsName('json_ext')

    @classmethod
    def create_element(cls, rule, namespace):
        """Creates the dictionary with the dump and load functions"""

        return {'loads': try_to_eval(rule.json_ext.loads,
                                     functions(namespace)),
                'dumps': try_to_eval(rule.json_ext.dumps,
                                     functions(namespace))}

    @classmethod
    def add_info_to_field(cls, json_id, rule):
        """Adds to the field definition the path to get the json functions"""
        info = {'dumps': None, 'loads': None}
        if 'json_ext' in rule:
            info['dumps'] = (json_id, 'json_ext', 'dumps')
            info['loads'] = (json_id, 'json_ext', 'loads')
        return info

    @classmethod
    def evaluate(cls, json, field_name, action, args):
        """Evaluate the dumps and loads functions depending on the action"""
        from invenio.modules.jsonalchemy.parser import FieldParser
        if action == 'set':
            try:
                json._dict[field_name] = reduce(
                    lambda obj, key: obj[key],
                    args['dumps'],
                    FieldParser.field_definitions(
                        json.additional_info.namespace))(json._dict_bson[field_name])
            except (KeyError, IndexError, TypeError, AttributeError):
                json._dict[field_name] = json._dict_bson[field_name]
        elif action == 'get':
            try:
                json._dict_bson[field_name] = reduce(
                    lambda obj, key: obj[key],
                    args['loads'],
                    FieldParser.field_definitions(
                        json.additional_info.namespace))(json._dict[field_name])
            except (KeyError, IndexError, TypeError):
                json._dict_bson[field_name] = json._dict[field_name]

parser = JsonExtraParser
