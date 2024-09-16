from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_page_number(self, request, paginator):
        """
        Override the default `get_page_number` to make the pagination start at index 0.
        """
        page_number = request.query_params.get(self.page_query_param, 0)
        
        try:
            # Convert page_number to an integer and add 1 to shift the pagination starting from 0
            page_number = int(page_number) + 1
        except ValueError:
            page_number = 1

        return page_number
    

    