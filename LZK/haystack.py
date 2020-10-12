from django.db.models.signals import m2m_changed, post_delete, post_save
from haystack.signals import BaseSignalProcessor


class SignalProcessor(BaseSignalProcessor):
    def setup(self):
        # Naive (listen to all model saves).
        post_save.disconnect(self.handle_save)
        post_delete.disconnect(self.handle_delete)
        for using in self.connection_router.for_write():
            indexes = self.connections[using].get_unified_index().get_indexes()
            for model, index in indexes.items():
                post_save.connect(self.handle_save, sender=model)
                post_delete.connect(self.handle_delete, sender=model)
                for related in model._meta.many_to_many:
                    through = getattr(model, related.get_attname())
                    m2m_changed.connect(self.handle_m2m, sender=through)
        # Efficient would be going through all backends & collecting all models
        # being used, then hooking up signals only for those.

    def teardown(self):
        # Naive (listen to all model saves).
        post_save.disconnect(self.handle_save)
        post_delete.disconnect(self.handle_delete)
        # Efficient would be going through all backends & collecting all models
        # being used, then disconnecting signals only for those.

    def handle_m2m(self, sender, instance, action, reverse, model, **kwargs):
        pass
