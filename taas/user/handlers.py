from django.forms import model_to_dict


def send_emails_to_users(sender, instance=None, created=False, **kwargs):
    if created:
        instance.email_user_on_registration()
        instance.email_admin_on_registration()

    old_active = instance._old_values['is_active']
    new_active = instance.is_active

    if (old_active, new_active) == (False, True):
        instance.email_user_on_activation()
    elif (old_active, new_active) == (True, False):
        instance.email_user_on_deactivation()


def preserve_fields_before_update(sender, instance, **kwargs):
    if instance.pk is None:
        return

    meta = instance._meta
    old_instance = meta.model._default_manager.get(pk=instance.pk)

    excluded_fields = [field.name for field in meta.many_to_many]
    excluded_fields.append(meta.pk.name)
    old_values = model_to_dict(old_instance, exclude=excluded_fields)

    setattr(instance, '_old_values', old_values)
