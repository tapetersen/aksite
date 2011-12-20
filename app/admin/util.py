from django.contrib import admin

class DefaultListFilter(admin.SimpleListFilter):
    """A list filter with a default.
        Set the default attribute and don't forget to include
        "all" in you lookups
    """
    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup or (
                        self.value() is None and lookup==self.default),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }
    def value(self):
        return self.used_parameters.get(self.parameter_name, self.default)
    
"""  
class InitialFieldsMixin(object):
    def get_form(self, request, obj=None, **kwargs):
        form = admin.ModelAdmin.get_form(self, request, obj, **kwargs)
        if not hasattr(self.__class__, 'initial'):
            return form

        old_init = form.__init__
        def new_init(_self, *args, **kwargs):
            if 'instance' not in kwargs:
                for field_name, callback in self.__class__.initial.iteritems():
                    kwargs['initial'][field_name] = callback(self, request,
                                                             obj, **kwargs)
            return old_init(_self, *args, **kwargs)
        form.__init__ = new_init

        return form
"""