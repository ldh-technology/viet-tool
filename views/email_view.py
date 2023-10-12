import time
import json

from typing import List
from nicegui import ui

# from services.email import list_of_emails
import models

columns = [
    # {'name': 'id', 'label': 'Id', 'field': 'id'},
    {'name': 'email', 'label': 'Email', 'field': 'email', 'required': True},
    {'name': 'secret_code', 'label': 'Secret Code',
        'field': 'secret_code', 'sortable': True},
    {'name': 'email_list', 'label': 'Email List',
        'field': 'email_list', 'sortable': True},
    {'name': 'actions', 'label': 'Actions',
        'field': 'actions'},
]


@ui.refreshable
async def list_of_emails() -> None:
    async def delete(id: int) -> None:
        email = await models.Email.get(id=id)
        await email.delete()
        list_of_emails.refresh()

    emails: List[models.Email] = await models.Email.all()
    email_rows = [email.as_dict() for email in emails]

    with ui.table(title='Email List', columns=columns, rows=email_rows, pagination=5).classes('w-full') as table:
        with table.add_slot('top-right'):
            with ui.input(placeholder='Tìm kiếm').props('type=search').bind_value(table, 'filter').add_slot('append'):
                ui.icon('search')
            table.add_slot('body-cell-actions', r'''
                    <q-td :props="props">
                        <q-btn size="sm" color="blue"
                            @click="$parent.$emit('run-edit',props.row)"
                            label="Sửa"
                            />
                            <q-btn size="sm" color="red"
                            @click="$parent.$emit('run-delete',props.row)"
                            label="Xoá"
                            />
                    </q-td>
            ''')
            table.on('run-edit', lambda msg: youedit(msg))
            table.on('run-delete', lambda msg: youdelete(msg))

    # for email in reversed(emails):
    #     with ui.card():
    #         with ui.row().classes('items-center'):
    #             ui.input('Name', on_change=email.save) \
    #                 .bind_value(email, 'email').on('blur', list_of_emails.refresh).classes('w-150')
    #             ui.input('Mã Bảo Mật', on_change=email.save) \
    #                 .bind_value(email, 'secret_code').on('blur', list_of_emails.refresh).classes('w-150')
    #             ui.input('Email list', on_change=email.save) \
    #                 .bind_value(email, 'email_list').on('blur', list_of_emails.refresh).classes('w-150')
    #             ui.button(icon='delete',
    #                       on_click=lambda u=email: delete(u)).props('flat')


    def youedit(msg):
        print(msg)


    async def youdelete(msg):
        data = msg.args
        print(data["id"])
        # email = models.Email(id=int(data["id"]), email=data["email"],secret_code=data["secret_code"],email_list=data["email_list"])
        # print(email)
        await delete(int(data["id"]))
        


async def index():
    async def create() -> None:
        print('create')
        try:
            await models.Email.create(email=email.value, secret_code=secret_code.value or '', email_list=email_list.value)
        except ValueError:
            print(ValueError)
        email.value = ''
        secret_code.value = ''
        email_list.value = None
        list_of_emails.refresh()

    with ui.column().classes('mx-auto'):
        with ui.row().classes('w-full items-center px-4'):
            email = ui.input(label='Email')
            secret_code = ui.input(label='Mã Bảo Mật')
            email_list = ui.input(
                label='Email list')
            ui.button(on_click=create, icon='add').props(
                'flat').classes('ml-auto')
        await list_of_emails()
