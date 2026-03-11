from auditlog.signals import post_log
from django.dispatch import receiver
import logging

logger = logging.getLogger("auditlog")

@receiver(post_log)
def log_audit_event(sender, instance, action, changes, actor=None, **kwargs):
    logger.info(
        f"User={actor} Action={action} Model={sender.__name__} ObjectID={instance.pk} Changes={changes}"
    )