import os
import sys
from scrapy.cmdline import execute

os.chdir(os.path.dirname(os.path.realpath(__file__)))

scrapy_file_name = sys.argv[1]

try:
    execute(
        [
            'scrapy',
            'runspider',
            scrapy_file_name,
        ]
    )
except SystemExit:
    pass

