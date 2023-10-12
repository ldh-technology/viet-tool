import models
from typing import List
from schemas.donhang import Donhang

# async def list_of_emails(search_text: str, limit: int, offset):
    
#     emails: List[models.Email] = await models.Email.all()
#     return emails


async def list_of_donhangs():
    
    donhangs: List[models.Donhang] = await models.Donhang.all()
    return donhangs


async def save_donhang(donhang: Donhang):
    print(donhang.thongtin)
    await models.Donhang.create(taikhoan=donhang.taikhoan, tensp=donhang.tensp,thongtin=donhang.thongtin,
                                tongtien=donhang.tongtien,link_sp=donhang.link_sp,order_number=donhang.order_number
                                ,item_number=donhang.item_number,date_sold=donhang.date_sold,soluong=donhang.soluong)
    # users: List[models.Donhang] = await models.Donhang.all()
    # return users
