from aiogram import Router

# Создание роутеров
start_router = Router()
menu_router = Router()
assignments_router = Router()
events_router = Router()

__all__ = [
    'start_router',
    'menu_router',
    'assignments_router',
    'events_router'
] 