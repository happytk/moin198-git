# -*- coding: UTF-8 -*-

"""
    MoinMoin - SQL

"""

from MoinMoin.parser._ParserBase import ParserBase

Dependencies = []

class Parser(ParserBase):

    parsername = "ColorizedSQL"
    extensions = ['.sql', '.pkb']
    Dependencies = []
    
    def __init__(self, raw, request, **kw):
        ParserBase.__init__(self,raw,request,**kw)
        self._ignore_case = 1

    def setupRules(self):
        ParserBase.setupRules(self)

        self.addRulePair("Comment","/[*]","[*]/")
        self.addRule("Comment","--.*$")
        self.addRulePair("String","L?['\"]",r"$|[^\\](\\\\)*['\"]")
        self.addRule("Number",r"[0-9](\.[0-9]*)?(eE[+-][0-9])?[flFLdD]?|0[xX][0-9a-fA-F]+[Ll]?")
        self.addRule("ID","[a-zA-Z_][0-9a-zA-Z_]*")
        self.addRule("SPChar",r"[~!%^&*()+=|\[\]:;,.<>/?{}-]")

        reserved_words = ['all', 'alter', 'and', 'any', 'array', 'as', 'asc', 'at',
              'authid', 'avg', 'begin', 'between', 'binary_integer', 'body',
              'boolean', 'bulk', 'by', 'case', 'char', 'char_base', 'check',
              'close', 'cluster', 'coalesce', 'collect', 'comment', 'commit',
              'compress', 'connect', 'constant', 'create', 'current', 'currval',
              'cursor', 'date', 'day', 'declare', 'decimal', 'default', 'delete',
              'desc', 'distinct', 'do', 'drop', 'else', 'elsif', 'end', 'exception',
              'exclusive', 'execute', 'exists', 'exit', 'extends', 'extract',
              'false', 'fetch', 'float', 'for', 'forall', 'from', 'function', 'goto',
              'group', 'having', 'heap', 'hour', 'if', 'immediate', 'in', 'index',
              'indicator', 'insert', 'integer', 'interface', 'intersect', 'interval',
              'into', 'is', 'isolation', 'java', 'level', 'like', 'limited', 'lock',
              'long', 'loop', 'max', 'min', 'minus', 'minute', 'mlslabel', 'mod',
              'mode', 'month', 'natural', 'naturaln', 'new', 'nextval', 'nocopy',
              'not', 'nowait', 'null', 'nullif', 'number', 'number_base', 'ocirowid',
              'of', 'on', 'opaque', 'open', 'operator', 'option', 'or', 'order',
              'organization', 'others', 'out', 'package', 'partition', 'pctfree',
              'pls_integer', 'positive', 'positiven', 'pragma', 'prior', 'private',
              'procedure', 'public', 'raise', 'range', 'raw', 'real', 'record',
              'ref', 'release', 'return', 'reverse', 'rollback', 'row', 'rowid',
              'rownum', 'rowtype', 'savepoint', 'second', 'select', 'separate',
              'set', 'share', 'smallint', 'space', 'sql', 'sqlcode', 'sqlerrm',
              'start', 'stddev', 'subtype', 'successful', 'sum', 'synonym',
              'sysdate', 'table', 'then', 'time', 'timestamp', 'timezone_region',
              'timezone_abbr', 'timezone_minute', 'timezone_hour', 'to', 'trigger',
              'true', 'type', 'uid', 'union', 'unique', 'update', 'use', 'user',
              'validate', 'values', 'varchar', 'varchar2', 'variance', 'view',
              'when', 'whenever', 'where', 'while', 'with', 'work', 'write', 'year',
              'zone' ]

        self.addReserved(reserved_words)
