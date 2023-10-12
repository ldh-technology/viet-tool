from tortoise import fields, models


class Email(models.Model):
    id = fields.IntField(pk=True)
    email= fields.CharField(max_length=50)
    secret_code= fields.CharField(max_length=50)
    email_list= fields.TextField()

    def __str__(self):
        return f"{self.id} | {self.email} | {self.email_list}"
    
    def as_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "secret_code": self.secret_code,
            "email_list": self.email_list,
            "actions": ["edit", "delete"]
        }


class Donhang(models.Model):
    id = fields.IntField(pk=True)
    taikhoan= fields.CharField(max_length=50)
    tensp= fields.CharField(max_length=200)
    thongtin= fields.CharField(max_length=500)
    tongtien= fields.CharField(max_length=20)
    link_sp= fields.CharField(max_length=1000)
    order_number= fields.CharField(max_length=50)
    item_number= fields.CharField(max_length=50)
    date_sold= fields.CharField(max_length=50)
    soluong= fields.IntField()

    def __str__(self):
        return f"{self.id} | {self.taikhoan} | {self.thongtin}"
    
    def as_dict(self):
        return {
            "id": self.id,
            "taikhoan": self.taikhoan,
            "tensp": self.tensp,
            "thongtin": self.thongtin,
            "tongtien": self.tongtien,
            "link_sp": self.link_sp,
            "order_number": self.order_number,
            "item_number": self.item_number,
            "item_number": self.item_number,
            "date_sold": self.date_sold,
            "soluong": self.soluong,
        }