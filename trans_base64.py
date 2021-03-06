#!/usr/bin/env python

import base64
import cStringIO
import re
def decodeMimeData(message):
    message_file = cStringIO.StringIO(message)
    header_dict = {}
    for line in message_file:
        if ":" in line:
            header, _, value = line.partition(":")
            header_dict[header] = value
        elif line == "\n":
            break
        else:
            raise Exception("Error when passing the header of POP3 response: %s"%line)

    match_obj = re.search("charset=(?P<codec>)", header_dict.get("Content-Type"))
    data_encoding = match_obj.group("codec") if match_obj else "GBK"
    return base64.decodestring(message_file.read().rstrip("\r\n.\r\n")).decode(data_encoding)
