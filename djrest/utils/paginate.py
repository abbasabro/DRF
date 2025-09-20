from rest_framework.pagination import PageNumberPagination,CursorPagination
from rest_framework.exceptions import ValidationError
from django.core.paginator import EmptyPage
#1.PageNumberPagination

class LargeResultsSetPaginator(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 10000
class StandardResultsSetPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

#2.CursorPagination(Secure URL from webScrappers) 
class CustomCursorPagination(CursorPagination):
    page_size = 10
    ordering = 'name' #must be a common field present in all models if the paginator is for general use
    max_page_size = 100

#3.Custom Paginator:
def paginate(data, paginator , pagenumber):
    #To Check if Enough pages
    if int(pagenumber) > paginator.num_pages:
        raise ValidationError("Not Enough Pages",code=404)
    
    #To Availabilty of previous page
    try:
        previous_page_number = paginator.page(pagenumber).previous_page_number()
    except EmptyPage:
        previous_page_number = None
    #To Availabilty of next page
    try:
        next_page_number = paginator.page(pagenumber).next_page_number()
    except EmptyPage:
        next_page_number = None
    
    data_to_show = paginator.page(pagenumber).object_list

    return {
        'pagination':{
            'previous_page_number':previous_page_number,
            'is_previous':paginator.page(pagenumber).has_previous(),
            'next_page_number':next_page_number,
            'is_next':paginator.page(pagenumber).has_next(),
            'start_index':paginator.page(pagenumber).start_index(),
            'end_index':paginator.page(pagenumber).end_index(),
            'total_entries':paginator.count,
            'total_pages':paginator.num_pages,
            'page':pagenumber,
        },
        'results':data_to_show
    }
    
    