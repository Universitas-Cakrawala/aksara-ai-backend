from pydantic import BaseModel, conint


class PageParams(BaseModel):
    """Request query params for paginated API."""

    page: conint(ge=1) = 1  # type: ignore
    size: conint(ge=1) = 10  # type: ignore


def MapPagination(data, totalItems, pageParams):
    return {
        "data": data,
        "pagination": {
            "total_items": totalItems,
            "page": pageParams.page,
            "size": pageParams.size,
            "total_pages": (totalItems + pageParams.size - 1)
            // pageParams.size,  # Calculate total pages
        },
    }
