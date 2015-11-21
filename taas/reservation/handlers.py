from taas.reservation.models import Payment


def delete_payment_before_last_reservation_delete(sender, instance=None, **kwargs):
    payment = instance.payment
    if payment is None:
        return
    elif payment.reservation_set.count() == 1 and payment.type == Payment.STAGED:
            instance.payment.delete()
