from pydantic import BaseModel

class Donhang(BaseModel):
    id: int | None
    taikhoan: str
    tensp: str
    thongtin: str
    tongtien: str
    link_sp: str
    order_number: str
    item_number: str
    date_sold: str
    soluong: str
    
    def __str__(self):
        return f"{self.id} | {self.taikhoan} | {self.thongtin}"
