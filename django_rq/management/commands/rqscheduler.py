from django.core.management.base import BaseCommand
from django_rq import get_scheduler
import logging
from optparse import make_option
from rq.utils import ColorizingStreamHandler


# Setup logging for RQScheduler if not already configured
logger = logging.getLogger('rq_scheduler')
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s %(message)s',
                                  datefmt='%H:%M:%S')
    handler = ColorizingStreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    

class Command(BaseCommand):
    """
    Runs RQ scheduler
    """
    help = __doc__
    args = '<queue>'

    option_list = BaseCommand.option_list + (
        make_option(
            '--interval',
            type=int,
            dest='interval',
            default=60,
            help="How often the scheduler checks for new jobs to add to the "
                 "queue (in seconds).",
        ),
    )

    def handle(self, queue='default', *args, **options):
        scheduler = get_scheduler(name=queue, interval=options.get('interval'))
        scheduler.run()
