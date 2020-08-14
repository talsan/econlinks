import os
from dotenv import load_dotenv

load_dotenv()

class Local:
    MULTIPROCESS_ON = True
    MULTIPROCESS_CPUS = None # None defaults to mp.cpu_count()


class Aws:
    # aws config
    AWS_KEY = os.environ.get('AWS_KEY')
    AWS_SECRET = os.environ.get('AWS_SECRET')

    S3_REGION_NAME = 'us-west-2'
    S3_FOOLCALLS_BUCKET = 'fool-calls'
    S3_OBJECT_ROOT = 'https://s3.console.aws.amazon.com/s3/object'

    ATHENA_REGION_NAME = 'us-west-2'
    ATHENA_WORKGROUP = 'qc'
    ATHENA_OUTPUT_BUCKET = 'fool-calls-athena-output'

    ATHENA_SLEEP_BETWEEN_REQUESTS = 3
    ATHENA_QUERY_TIMEOUT = 200

class AlphaVantage():
    AV_KEY = os.environ.get('AV_KEY')

class FoolCalls:

    SCRAPER_VERSION = '202007.1'

    # fixed ishares.com values, the rest is derived/scraped
    ROOT = 'https://www.fool.com'
    EARNINGS_LINKS_ROOT = f'{ROOT}/earnings-call-transcripts'
    EARNINGS_TRANSCRIPTS_ROOT = f'{ROOT}/earnings/call-transcripts'
