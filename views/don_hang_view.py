import time
import json

from typing import List
from nicegui import ui

from services.donhang_services import list_of_donhangs
from services.get_content_email import get_don_hang
import models

columns = [
    # {'name': 'id', 'label': 'Id', 'field': 'id'},
    {'name': 'taikhoan', 'label': 'Tài khoản', 'field': 'taikhoan', 'sortable': True, 'align': 'center'},
    {'name': 'tensp', 'label': 'Tên SP',
        'field': 'tensp', 'sortable': True, 'align': 'center'},
    {'name': 'thongtin', 'label': 'Thông tin',
        'field': 'thongtin', 'sortable': True, 'align': 'center'},
    {'name': 'tongtien', 'label': 'Tổng tiền',
        'field': 'tongtien', 'sortable': True, 'align': 'center'},
    {'name': 'link_sp', 'label': 'Link SP',
        'field': 'link_sp', 'sortable': True, 'align': 'center'},
    {'name': 'order_number', 'label': 'Order Number',
        'field': 'order_number', 'sortable': True, 'align': 'center'},
    {'name': 'item_number', 'label': 'Item No',
        'field': 'item_number', 'sortable': True, 'align': 'center'},
    {'name': 'date_sold', 'label': 'Date Sold',
        'field': 'date_sold', 'sortable': True, 'align': 'center'},
    {'name': 'soluong', 'label': 'Số Lượng',
        'field': 'soluong', 'sortable': True, 'align': 'center'},
    {'name': 'actions', 'label': 'Actions',
        'field': 'actions', 'align': 'center'},
]


async def index():
    with ui.column().classes('mx-auto'):
        with ui.row().classes('w-full items-center px-4'):
            ui.button('Lấy đơn hàng', on_click=lambda: get_don_hang_view()).classes('w-32')
        await list_of_donhangs_view()
        
async def get_don_hang_view():
    result = await get_don_hang()
    # if result["code"] == "SUCCESS":
    print('abca2')
    with ui.dialog() as dialog, ui.card():
        ui.label(result["message"])
        ui.button('Đóng', on_click=dialog.close)
    await dialog
    list_of_donhangs_view.refresh()
    # await show_dialog(result["message"])
    
@ui.refreshable
async def list_of_donhangs_view() -> None:
    async def delete(id: int) -> None:
        donhang = await models.Donhang.get(id=id)
        await donhang.delete()
        list_of_donhangs_view.refresh()

    donhangs: List[models.Donhang] = await models.Donhang.all()
    donhang_rows = [donhang.as_dict() for donhang in donhangs]

    with ui.table(title='Email List', columns=columns, rows=donhang_rows, pagination=5).classes('w-full') as table:
        with table.add_slot('top-right'):
            with ui.input(placeholder='Tìm kiếm').props('type=search').bind_value(table, 'filter').add_slot('append'):
                ui.icon('search')
            table.add_slot('body-cell-actions', r'''
                    <q-td :props="props">
                            <q-btn size="sm" color="red"
                            @click="$parent.$emit('run-delete',props.row)"
                            label="Xoá"
                            />
                    </q-td>
            ''')
            table.add_slot('body-cell-link_sp', r'''
                    <q-td :props="props">
                        <a target="_blank" :href="props.row.link_sp">Link</a>
                    </q-td>
            ''')
            table.on('run-delete', lambda msg: youdelete(msg))

    async def youdelete(msg):
        data = msg.args
        print(data["id"])
        # email = models.Donhang(id=int(data["id"]), email=data["email"],secret_code=data["secret_code"],email_list=data["email_list"])
        # print(email)
        await delete(int(data["id"]))
        

