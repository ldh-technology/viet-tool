from router import Router

from nicegui import app, ui
from tortoise.contrib.fastapi import register_tortoise
from views import email_view, don_hang_view

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},  # tortoise will look for models in this main module
    generate_schemas=True,  # in production you should use version control migrations instead
)


@ui.page('/')  # normal index page (e.g. the entry point of the app)
@ui.page(
    '/{_:path}')  # all other pages will be handled by the router but must be registered to also show the SPA index page
def main():
    router = Router()

    @router.add('/')
    async def show_one():
        await email_view.index()

    @router.add('/don-hang')
    async def show_two():
        await don_hang_view.index()

    # adding some navigation buttons to switch between the different pages
    with ui.row():
        ui.button('Email', on_click=lambda: router.open(show_one)).classes('w-32')
        ui.button('Đơn Hàng', on_click=lambda: router.open(show_two)).classes('w-32')

    # this places the content which should be displayed
    router.frame().classes('w-full p-4 bg-gray-100')


# ui.button('enlarge', on_click=lambda: app.native.main_window.resize(1000, 700))

# ui.run(native=True, window_size=(1000, 700), fullscreen=False)
ui.run(native=True, window_size=(1000, 700))