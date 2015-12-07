import logging

from celery import shared_task
from django.utils import timezone

from taas.reservation import models


logger = logging.getLogger(__name__)


@shared_task
def remove_expired_reservations():
    limit_date = timezone.now() - timezone.timedelta(minutes=10)
    unpaid_reservations = models.Reservation.objects.filter(paid=False,
                                                            date_created__lt=limit_date)
    if unpaid_reservations.exists():
        unpaid_reservations.delete()
        logger.info("Expired unpaid reservations has been removed.")
    else:
        logger.info("There are no expired unpaid reservations.")

