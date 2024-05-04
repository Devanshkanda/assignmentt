from fastapi.routing import APIRouter
from fastapi import HTTPException
from seed import get_bank_names_and_ids, get_branch_details, cached_bank_ids_and_names
from functools import lru_cache

router = APIRouter(
    prefix="/api/v1/banks"
)

@lru_cache(maxsize=180)
@router.get("/lists/", 
            status_code=200, 
            summary="this method will fetch bank names and their id's. if successfully found it will return 200 response else a 404 not found",
            tags=['Bank Lists']
)
async def get_banks_list():
    """
    This route method is used to get all the Bank Names and their Id's.

    first it will check for cached result in lru cache or cached_bank_ids_and_names dictionary.
    if found it will return response quicky. else it will perform the operaion for find, collect, organise
    the data and return the resulted dictionary
    """

    print("in views", cached_bank_ids_and_names)
    if bool(cached_bank_ids_and_names):
        print("i am in cache dictionary")
        return {
            "status": 200,
            "message": "Bank ids and Bank names data fetched successfully",
            "Format": {
                "Bank id": "bank name"
            },
            "data": cached_bank_ids_and_names
        }
    
    list_of_banks: dict = get_bank_names_and_ids()

    if not list_of_banks:
        raise HTTPException(
            404,
            {
                "status": 404,
                "message": "sorry no bank details found"
            }
        )
    
    list_of_banks.pop("bank_id")

    return {
        "status": 200,
        "message": "Bank ids and Bank names data fetched successfully",
        "Format": {
            "Bank id": "bank name"
        },
        "data": (list_of_banks)
    }

@lru_cache
@router.get("/branch/{ifsc}/details/", 
            status_code=200, 
            summary="this method will fetch branch details. if successfully found it will return 200 response else 404",
            tags=['Bank Branch Details'])
async def get_bank_branch_details(ifsc: str):
    """
    This route method is used to fetch all the details of a perticular Bank's specific Branch

    It will fetch IFSC Code from the user in the query parameter as IFSC Code is Unique, and can
    uniquely identify a specific bank's Branch Details

    first it will make a lookup for the perticular record existance in the lru cache, if not found
    then it will perform the operation to search for details by reading from csv file and save the result
    in lru cache for future access
    """

    branch_details = get_branch_details(ifsc_code=ifsc)

    if not branch_details:
        raise HTTPException(
            status_code=404,
            detail={
                "status": 404,
                "message": "Sorry no branch details found!"
            }
        )
    
    return {
        "status": 200,
        "message": "branch details fetched successfully",
        "data": {
            "ifsc code": branch_details[0],
            "bank id": branch_details[1],
            "bank name": branch_details[7],
            "branch": branch_details[2],
            "address": branch_details[3],
            "city": branch_details[4],
            "district": branch_details[5],
            "state": branch_details[6]
        }
    }