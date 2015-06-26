from .base import Action

import servant.fields


class PaginationField(servant.fields.ContainerField):
    page = servant.fields.IntField(min_value=1)
    page_size = servant.fields.IntField(min_value=1)
    num_pages = servant.fields.IntField()
    total_count = servant.fields.IntField()


class PaginatedActionMixin(Action):
    # Input controls...page is 1-based
    page = servant.fields.IntField(default=1, min_value=1)
    page_size = servant.fields.IntField(default=25, min_value=1)

    # Output
    paging = servant.fields.ModelField(PaginationField, in_response=True)

    def init_paging(self):
        # set an empty paging field
        self.paging = PaginationField({
            'page': self.page,
            'page_size': self.page_size,
        })

    def get_pagination_indices(self, offset=0, limit=None):
        # Since page is 1-based, bump it down
        page = self.page - 1
        offset = offset or (page * self.page_size)
        limit = limit or (offset + self.page_size)
        return (offset, limit)

    def paginate(self, listing):
        """Apply the pagination

        Every service may paginate differently, so this method needs to be implemented
        specficically for each service or action.

        """
        raise NotImplementedError('Subclasses must implement this method')
