from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.models import AssignmentStatus

SUBJECT_NAMES = {
    "programming": "Программирование",
    "informatics": "Информатика",
    "discrete_math": "Дискретная математика"
}

def get_subject_name(subject_code: str) -> str:
    return SUBJECT_NAMES.get(subject_code, subject_code)

def get_assignment_type_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Лабораторная работа", callback_data="assignment_type:lab"),
        InlineKeyboardButton(text="Домашнее задание", callback_data="assignment_type:homework")
    )
    return builder.as_markup()

def get_assignments_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Добавить задание", callback_data="assignment:add"),
        InlineKeyboardButton(text="Список заданий", callback_data="assignment:list"),
        InlineKeyboardButton(text="Дедлайны", callback_data="assignment:deadlines"),
        InlineKeyboardButton(text="Назад", callback_data="menu:back")
    )
    builder.adjust(1)
    return builder.as_markup()

def get_assignment_actions_kb(assignment_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Изменить статус", callback_data=f"assignment:change_status:{assignment_id}"),
        InlineKeyboardButton(text="Удалить", callback_data=f"assignment:delete:{assignment_id}"),
        InlineKeyboardButton(text="Назад", callback_data="assignment:list")
    )
    builder.adjust(1)
    return builder.as_markup()

def get_status_text(status: AssignmentStatus) -> str:
    status_texts = {
        AssignmentStatus.NOT_STARTED: "Не начато",
        AssignmentStatus.IN_PROGRESS: "В работе",
        AssignmentStatus.COMPLETED: "Готово",
        AssignmentStatus.SUBMITTED: "Сдано"
    }
    return status_texts[status]

def get_status_choice_kb(assignment_id: str):
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"⏳ {get_status_text(AssignmentStatus.NOT_STARTED)}", 
                callback_data=f"status:not_started:{assignment_id}"
            ),
            InlineKeyboardButton(
                text=f"🔄 {get_status_text(AssignmentStatus.IN_PROGRESS)}", 
                callback_data=f"status:in_progress:{assignment_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"✅ {get_status_text(AssignmentStatus.COMPLETED)}", 
                callback_data=f"status:completed:{assignment_id}"
            ),
            InlineKeyboardButton(
                text=f"📤 {get_status_text(AssignmentStatus.SUBMITTED)}", 
                callback_data=f"status:submitted:{assignment_id}"
            )
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data=f"assignment:view:{assignment_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_assignment_list_kb(assignments: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for assignment_id, assignment in assignments.items():
        builder.add(
            InlineKeyboardButton(
                text=f"{'🔬' if assignment.type == 'lab' else '📚'} {assignment.name}",
                callback_data=f"assignment:view:{assignment_id}"
            )
        )
    builder.add(InlineKeyboardButton(text="Назад", callback_data="menu:back"))
    builder.adjust(1)
    return builder.as_markup()

def get_subject_choice_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=SUBJECT_NAMES["programming"], callback_data="subject:programming"),
        InlineKeyboardButton(text=SUBJECT_NAMES["informatics"], callback_data="subject:informatics"),
        InlineKeyboardButton(text=SUBJECT_NAMES["discrete_math"], callback_data="subject:discrete_math")
    )
    builder.adjust(1)
    return builder.as_markup()
