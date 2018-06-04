from typing import Tuple


class CobwebModelMixin:
    name_fields: Tuple[str, ...] = ('title',)
    pk: int
    _meta: object

    def make_name(self, exclude=set(), sep='\n'):
        return sep.join([
            str(getattr(self, field_name)) for field_name in self.name_fields
            if hasattr(self, field_name) and field_name not in exclude
        ])
    
    @property
    def name(self):
        if not hasattr(self, '_name'):
            self._name = self.make_name()
        return self._name
    
    def __str__(self) -> str:
        """
        Return a string representation of project.
        """
        return (self.make_name(sep=' - ') or
                f'{self._meta.verbose_name.capitalize} {self.pk}' or
                f'Unsaved {self._meta.verbose_name.capitalize}')

    def __repr__(self):
        parts: It = [self.__class__.__name__, str(self.pk)]

        if self.name_fields:
            parts[1] += ':'
            parts.extend(
                *[f'{f}={getattr(self, f)}' for f in self.name_fields]
            )

        return f'<{" ".join(parts)}>'
