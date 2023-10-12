import models
from typing import List


# async def list_of_emails(search_text: str, limit: int, offset):
    
#     emails: List[models.Email] = await models.Email.all()
#     return emails


async def list_of_emails():
    
    emails: List[models.Email] = await models.Email.all()
    return emails


async def save_email():
    
    users: List[models.User] = await models.User.all()
    return users
