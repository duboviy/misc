#!/usr/bin/env python
import argparse
import glob
import logging
import os
import fnmatch
import shutil
import StringIO


class Tabs2SpaceConverter(object):
    """ Convert tabs to spaces in text/source files. """
    def __init__(self, path=('.',), tab_stop=4, extension='*.py', pretend=False, log_level='DEBUG'):
        self.files_processed = 0

        self.path = path
        self.tab_stop = tab_stop
        self.pretend = pretend
        self.extension = extension
        self.log_level = log_level

        self._set_log()

    def _set_log(self):
        logger = logging.getLogger()
        logger.setLevel(self.log_level)

        fm = logging.Formatter('%(filename)s [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')

        console = logging.StreamHandler()
        console.setLevel(self.log_level)
        console.setFormatter(fm)

        logger.addHandler(console)

    def _prepare_path_list(self):
        logging.debug('path_arg: %s' % self.path)
        self.path_list = []

        for path in self.path:
            self.path_list.extend(glob.glob(path))

        logging.info('PATH: %s' % self.path_list)

    def _process_paths(self):
        for path in self.path_list:

            if os.path.isfile(path):
                self._process(path)

            elif os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for filename in fnmatch.filter(files, self.extension):
                        self._process(os.path.join(root, filename))
            else:
                raise TypeError('%s should be either dir or file' % path)

        if self.pretend:
            logging.info('No actual changes was done, run without \'-p\' to overwrite source files')

        logging.info('%d files processed' % self.files_processed)

    def _process(self, path_):
        filepath = os.path.abspath(path_)
        changed = self._tabs_to_spaces(filepath)

        if changed:
            self.files_processed += 1

    def _tabs_to_spaces(self, file_name):
        def process_line(line_):
            return line_.replace('\t', ' ' * self.tab_stop)

        logging.debug('Processing file: %s' % file_name)

        was_changed = False
        temp_file = StringIO.StringIO()

        with open(file_name) as f:
            for line in f:
                newline = process_line(line)

                if newline != line:
                    was_changed = True

                temp_file.write(newline)

        if was_changed:
            try:
                logging.debug('Replacing file %s' % file_name)

                if not self.pretend:
                    temp_file.seek(0)

                    with open(file_name, 'w') as f:
                        shutil.copyfileobj(temp_file, f)
            except IOError:
                import traceback
                traceback.print_exc()

        return was_changed

    def run(self):
        self._prepare_path_list()
        self._process_paths()


def parse_args():
    parser = argparse.ArgumentParser(description='Convert tabs to spaces in text/source files')

    parser.add_argument('path', type=str, nargs='+', help='Path to scan')
    parser.add_argument('--tabstop', '-t', type=int, help='Number of spaces to replace tab symbol', default=4)
    parser.add_argument('--pretend', '-p', action='store_true', help='Don\'t actually change anything')
    parser.add_argument('--extension', '-e', type=str, help='File extension to replace tab symbol', default='*.py')
    parser.add_argument('--loglevel', '-l', type=str, help='Logging level', default='DEBUG')

    return parser.parse_args()


if __name__ == '__main__':
    config = parse_args()

    t2sc = Tabs2SpaceConverter(path=config.path,
                               tab_stop=config.tabstop,
                               pretend=config.pretend,
                               extension=config.extension,
                               log_level=config.loglevel)
    t2sc.run()

    # Example of output (converting 2 folders with 6 python scripts):
    # C:\Anaconda2\python.exe tab2spaces.py C:\site\123 C:\site\123_1
    # tab2spaces.py[LINE:37]  # DEBUG    [2016-12-29 17:24:36,234]  path_arg: ['C:\\site\\123', 'C:\\site\\123_1']
    # tab2spaces.py[LINE:43]  # INFO     [2016-12-29 17:24:36,244]  PATH: ['C:\\site\\123', 'C:\\site\\123_1']
    # tab2spaces.py[LINE:73]  # DEBUG    [2016-12-29 17:24:36,244]  Processing file: C:\site\123\1 - (2).py
    # tab2spaces.py[LINE:73]  # DEBUG    [2016-12-29 17:24:36,244]  Processing file: C:\site\123\1.py
    # tab2spaces.py[LINE:89]  # DEBUG    [2016-12-29 17:24:36,244]  Replacing file C:\site\123\1.py
    # tab2spaces.py[LINE:73]  # DEBUG    [2016-12-29 17:24:36,244]  Processing file: C:\site\123_1\1 - (2).py
    # tab2spaces.py[LINE:73]  # DEBUG    [2016-12-29 17:24:36,244]  Processing file: C:\site\123_1\1.py
    # tab2spaces.py[LINE:89]  # DEBUG    [2016-12-29 17:24:36,244]  Replacing file C:\site\123_1\1.py
    # tab2spaces.py[LINE:60]  # INFO     [2016-12-29 17:24:36,244]  6 files processed
