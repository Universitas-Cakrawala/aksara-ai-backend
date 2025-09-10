from starlette import status
from datetime import datetime
import pytz

# Error Code
HTTP_BAD_REQUEST = status.HTTP_400_BAD_REQUEST
HTTP_INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR
HTTP_NOT_FOUND = status.HTTP_404_NOT_FOUND
HTTP_FORBIDDEN = status.HTTP_403_FORBIDDEN
HTTP_UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED

# Success Code
HTTP_OK = status.HTTP_200_OK
HTTP_CREATED = status.HTTP_201_CREATED
HTTP_ACCEPTED = status.HTTP_202_ACCEPTED


# Date
CURRENT_DATETIME = datetime.now(pytz.timezone("Asia/Jakarta"))

# MongoDB Variable
MONGO_DATABASE = "aiservicedb"  #! db name
MONGO_DOCUMENT_AI_JOBS_RESULTS = "aijobresults"  #! result extraction file
MONGO_DOCUMENT_AI_JOBS = "aijobs"  #! jobs status extraction results (finised or error)


MONTHS = [
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember",
]
