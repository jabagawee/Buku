#! /usr/bin/env python3

import os
import sys

from .bukuconstants import DELIM

PROMPTMSG = 'buku (? for help): '  # Prompt message string

# Default format specifiers to print records
ID_STR = '%d. %s [%s]\n'
ID_DB_STR = '%d. %s'
MUTE_STR = '%s (L)\n'
URL_STR = '   > %s\n'
DESC_STR = '   + %s\n'
TAG_STR = '   # %s\n'


class Formatter:
    def __init__(self,
                 id_str=ID_STR,
                 id_db_str=ID_DB_STR,
                 mute_str=MUTE_STR,
                 url_str=URL_STR,
                 desc_str=DESC_STR,
                 tag_str=TAG_STR,
                 prompt_msg=PROMPTMSG):
        self.id_str = id_str
        self.id_db_str = id_db_str
        self.mute_str = mute_str
        self.url_str = url_str
        self.desc_str = desc_str
        self.tag_str = tag_str
        self.prompt_msg = prompt_msg

    def print_rec_with_filter(self, records, field_filter=0):
        """Print records filtered by field.

        User determines which fields in the records to display
        by using the --format option.

        Parameters
        ----------
        records : list or sqlite3.Cursor object
            List of bookmark records to print
        field_filter : int
            Integer indicating which fields to print.
        """

        try:
            if field_filter == 0:
                for row in records:
                    self.print_single_rec(row)
            elif field_filter == 1:
                for row in records:
                    print('%s\t%s' % (row[0], row[1]))
            elif field_filter == 2:
                for row in records:
                    print('%s\t%s\t%s' % (row[0], row[1], row[3][1:-1]))
            elif field_filter == 3:
                for row in records:
                    print('%s\t%s' % (row[0], row[2]))
            elif field_filter == 4:
                for row in records:
                    print('%s\t%s\t%s\t%s' % (row[0], row[1], row[2], row[3][1:-1]))
            elif field_filter == 5:
                for row in records:
                    print('%s\t%s\t%s' % (row[0], row[2], row[3][1:-1]))
            elif field_filter == 10:
                for row in records:
                    print(row[1])
            elif field_filter == 20:
                for row in records:
                    print('%s\t%s' % (row[1], row[3][1:-1]))
            elif field_filter == 30:
                for row in records:
                    print(row[2])
            elif field_filter == 40:
                for row in records:
                    print('%s\t%s\t%s' % (row[1], row[2], row[3][1:-1]))
            elif field_filter == 50:
                for row in records:
                    print('%s\t%s' % (row[2], row[3][1:-1]))
        except BrokenPipeError:
            sys.stdout = os.fdopen(1)
            sys.exit(1)

    def print_single_rec(self, row, idx=0):  # NOQA
        """Print a single DB record.

        Handles both search results and individual record.

        Parameters
        ----------
        row : tuple
            Tuple representing bookmark record data.
        idx : int, optional
            Search result index. If 0, print with DB index.
            Default is 0.
        """

        str_list = []

        # Start with index and title
        if idx != 0:
            id_title_res = self.id_str % (idx, row[2] if row[2] else 'Untitled', row[0])
        else:
            id_title_res = self.id_db_str % (row[0], row[2] if row[2] else 'Untitled')
            # Indicate if record is immutable
            if row[5] & 1:
                id_title_res = self.mute_str % (id_title_res)
            else:
                id_title_res += '\n'

        str_list.append(id_title_res)
        str_list.append(self.url_str % (row[1]))
        if row[4]:
            str_list.append(self.desc_str % (row[4]))
        if row[3] != DELIM:
            str_list.append(self.tag_str % (row[3][1:-1]))

        try:
            print(''.join(str_list))
        except BrokenPipeError:
            sys.stdout = os.fdopen(1)
            sys.exit(1)
