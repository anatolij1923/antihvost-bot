from datetime import datetime, timedelta
from database import Database

class GroupTasksManager:
    def __init__(self, db: Database):
        self.db = db
        self.ivtb_labs = {
            "Программирование": [
                {
                    "title": "Исследование алгоритмов сортировки",
                    "description": "Лабораторная работа по исследованию различных алгоритмов сортировки",
                    "deadline": None,  # Будет установлен при добавлении
                    "priority": "🟡 Средний"
                },
                {
                    "title": "Реализация элементарных структур данных",
                    "description": "Лабораторная работа по реализации структур данных на основе динамической памяти",
                    "deadline": None,
                    "priority": "🟡 Средний"
                },
                {
                    "title": "Исследование фракталов",
                    "description": "Лабораторная работа по исследованию и визуализации фракталов",
                    "deadline": None,
                    "priority": "🟡 Средний"
                },
                {
                    "title": "Знакомство со средой программирования Delphi/Lazarus",
                    "description": "Лабораторная работа по освоению среды программирования Delphi/Lazarus",
                    "deadline": None,
                    "priority": "🟡 Средний"
                }
            ],
            "Информатика": [
                {
                    "title": "Светодиодные индикаторы",
                    "description": "Лабораторная работа по работе со светодиодными индикаторами",
                    "deadline": None,
                    "priority": "🟡 Средний"
                },
                {
                    "title": "ПЬЕЗОЭЛЕМЕНТ, МИКРОСХЕМЫ",
                    "description": "Лабораторная работа по работе с пьезоэлементами и микросхемами",
                    "deadline": None,
                    "priority": "🟡 Средний"
                },
                {
                    "title": "СВЕТОДИОДНЫЕ СБОРКИ",
                    "description": "Лабораторная работа по работе со светодиодными сборками",
                    "deadline": None,
                    "priority": "🟡 Средний"
                },
                {
                    "title": "ДИСПЛЕЙ, МОТОР, СВЕТОДИОДНЫЕ МАТРИЦЫ",
                    "description": "Лабораторная работа по работе с дисплеями, моторами и светодиодными матрицами",
                    "deadline": None,
                    "priority": "🟡 Средний"
                },
                {
                    "title": "СБОРКИ БЕЗ ПРОГРАММИРОВАНИЯ",
                    "description": "Лабораторная работа по сборке устройств без программирования",
                    "deadline": None,
                    "priority": "🟡 Средний"
                }
            ]
        }

    async def add_labs_for_new_student(self, user_id: int, group_name: str):
        """Добавляет лабораторные работы для нового студента ИВТб 1 курса"""
        if not group_name.startswith("ИВТб-1"):
            return False

        # Устанавливаем дедлайны для лабораторных работ
        current_date = datetime.now()
        for subject, labs in self.ivtb_labs.items():
            for i, lab in enumerate(labs):
                # Устанавливаем дедлайн через 2 недели от текущей даты для каждой работы
                deadline = current_date + timedelta(weeks=2 + i)
                lab["deadline"] = deadline

                # Добавляем лабораторную работу в базу данных
                success = await self.db.add_task(
                    user_id=user_id,
                    title=lab["title"],
                    task_type="🔬 Лабораторная",
                    subject=subject,
                    deadline=deadline,
                    description=lab["description"],
                    priority=lab["priority"]
                )
                if not success:
                    return False

        return True 