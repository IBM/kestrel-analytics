import base64
import json
import logging
import re

from lark import Lark, Transformer, exceptions
from urllib.parse import unquote

logger = logging.getLogger(__name__)


grammar = '''
// log4j substition parser

start: subst

subst: "${" prefix* cstr* default? "}"

cstr: subst|/[^$]/|NAME

default: ":-" (LETTER|DIGIT|OTHER)*

prefix: (NAME)? ":"

NAME: LETTER (LETTER|DIGIT|"_"|"-"|".")*

OTHER: "/"|"."|"_"|"-"|":"|" "

%import common (LETTER, DIGIT)
'''


class _TranslateTree(Transformer):
    def __init__(self):
        super().__init__()

    def start(self, arg):
        return arg[0]

    def subst(self, args):
        if args:
            bodies = []
            for a in args:
                if a[0] == "prefix":
                    bodies += a[1] + ":"
                elif a[0] == "cstr":
                    bodies += a[1]
                elif a[0] == "default":
                    bodies += ":-" + a[1]
                    
            body = "".join(bodies)
            
            if ":-" in body:
                bodies = body.split(":-")
                default = bodies[-1]
                body = ":-".join(bodies[:-1])
            else:
                default = None
                
            if ":" in body:
                bodies = body.split(":")
                prefix = bodies[0]
                body = ":".join(bodies[1:])
            else:
                prefix = None
                
            if prefix:
                if prefix == 'base64':
                    value = base64.b64decode(body).decode('utf-8')
                elif prefix == 'lower':
                    value = body.lower()
                elif prefix in ('jndi', 'sys'):
                    value = '${' + prefix + ":" + body + '}'
                elif default:
                    value = default
                else:
                    value = body
            elif default:
                value = default
            else:
                value = body
                    
            return value

        else:
            return ""

    def cstr(self, args):
        return ("cstr", ''.join(args))

    def default(self, args):
        if args:
            return ("default", ''.join(args))
        return ''

    def prefix(self, args):
        if args and args[0]:
            return ("prefix", args[0].value)
        return ''


parser = Lark(grammar, parser='lalr', # debug=True,
              transformer=_TranslateTree())


def deobfuscate(data):
    try:
        result = parser.parse(data.lower())
    except exceptions.UnexpectedToken as e:
        #logger.error('%s', e, exc_info=e)
        result = None
    return result


def check_string(s):
    # Check for a Java exception as a special case
    if re.match(r'.*Error looking up JNDI resource \[ldap:\/\/.+\/.*\].*', s):
        return s

    for match in re.findall(r'(\$\{.*\})', s):
        deob = deobfuscate(match.lower())
        if deob and deob.find('${jndi:') > -1:
            return deob
    return None


def check_url(url):
    # We run unencode 3 times to handle all known in-the-wild in-log encodings
    return check_string(unquote(unquote(unquote(url))))


def check_object(obj):
    result = None
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str):
                result = check_url(value)
                if result:
                    return result
            elif isinstance(value, (dict, list)):
                result = check_object(value)
                if result:
                    return result
    elif isinstance(obj, list):
        for item in obj:
            result = check_object(item)
            if result:
                return result
    elif isinstance(obj, str):
        result = check_url(obj)
    return result


def check_payload(payload_bin):
    # Hopefully this is a log payload and not a packet payload!
    payload = base64.b64decode(payload_bin).decode('utf-8')
    # Check if it's JSON
    try:
        payload = json.loads(payload)
        return check_object(payload)
    except json.decoder.JSONDecodeError:
        pass
    # Use check_url here in case there's some URL-encoding
    return check_url(payload)
