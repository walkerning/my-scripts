#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import os
import errno
import argparse

import chardet

if sys.version_info.major >= 3:
    raw_input = input
# ---- START CONSTS ----
# ---- consts for chardet ----
MIN_CONFIDENCE_TOLERENCE = 0.65

# ---- consts for confirmation ----
YES_CONFIRMATION_LIST = {'y', 'yes', 'Yes', 'YES', 'Y'}
NO_CONFIRMATION_LIST = {'n', 'no', 'No', 'NO', 'N'}

WRONG_CONFIRM = 0
YES_CONFIRM = 1
NO_CONFIRM = -1

# ---- END CONSTS ----


def main():
    parser = argparse.ArgumentParser(
        description="translate files/strings to another encoding"
    )

    detect_parser_group = parser.add_mutually_exclusive_group()
    detect_parser_group.add_argument('-d', '--detect-from', default=None)
    detect_parser_group.add_argument('-c', '--decoding-from', default=None)
    parser.add_argument(
        '--encoding-to', default='utf-8'
    )
    parser.add_argument(
        '-t', '--translate-to',
        default="/dev/stdout",
    )

    parser.add_argument(
        '-s', '--string-mode',
        action='store_const', const=True, default=False,
    )

    parser.add_argument(
        '-i', '--inplace',
        action='store_true',
        help='inplace modification, indicates: `TRANSLATE_TO == TRANSLATE_FROM`'
    )
    args, files = parser.parse_known_args()

    # get the content to be translated
    for translate_from in files:
        if not args.string_mode:
            if args.detect_from is not None:
                if not judge_isfile(args.detect_from):
                    print("Error: detect_from文件 '%s' 不存在. Abort!" % args.detect_from)
                    sys.exit(errno.ENOENT)
            else:
                args.detect_from = translate_from
            if not judge_isfile(translate_from):
                print("Error: translate_from文件 '%s' 不存在. Abort!" % translate_from)
                sys.exit(errno.ENOENT)
            translate_from_string = open(translate_from, 'rb').read()
            detect_from_string = open(args.detect_from, 'rb').read()
        else:
            translate_from_string = translate_from
            detect_from_string = args.detect_from or translate_from

        # determine the decoding codec
        if args.decoding_from is not None:
            decoding_codec = args.decoding_from
        else:
            detect_res = chardet.detect(detect_from_string)
            decoding_codec = detect_res['encoding']
            if detect_res['confidence'] < MIN_CONFIDENCE_TOLERENCE:
                confirm_code = judge_answer_code(("Error: detect encoding(判决为%s)得到的confidence太小(%.3f < %.3f)."
                                                  "要继续吗(y/n)> " % (decoding_codec,
                                                                      detect_res['confidence'],
                                                                      MIN_CONFIDENCE_TOLERENCE)))
                while confirm_code == WRONG_CONFIRM:
                    confirm_code = judge_answer_code(("Error: detect encoding(判决为%s)得到的confidence太小(%.3f < %.3f)."
                                                      "要继续吗(y/n)> " % (decoding_codec,
                                                                           detect_res['confidence'],
                                                                           MIN_CONFIDENCE_TOLERENCE)))
                if confirm_code == NO_CONFIRM:
                    sys.exit(255)

        if args.inplace:
            args.translate_to = translate_from
        # Start translating
        print("OK! Start translating %s, using decoding-from=%s, to encoding-to=%s\n"
              "----------------------------------------------------------------"
              % (translate_from, decoding_codec, args.encoding_to))
        if not args.string_mode and args.inplace:
            # backup the original file
            backup_file = args.translate_to + ".bak"
            with open(backup_file, 'wb') as bf:
                bf.write(translate_from_string)
        with open(args.translate_to, 'wb') as of:
            of.write(translate_from_string.decode(decoding_codec).encode(args.encoding_to))
        print("----------------------------------------------------------------\nFinish!")



def judge_isfile(file_name):
    return os.path.isfile(file_name)


def judge_answer_code(query):
    answer_code = input(query)
    if answer_code in YES_CONFIRMATION_LIST:
        return YES_CONFIRM
    elif answer_code in NO_CONFIRMATION_LIST:
        return NO_CONFIRM
    else:
        return WRONG_CONFIRM


if __name__ == "__main__":
    main()
