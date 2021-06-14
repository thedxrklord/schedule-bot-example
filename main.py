from datetime import datetime, timedelta
from itertools import islice

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from settings import *
from Schedule import Schedule

bot = telebot.TeleBot(telegramKey)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    schedule = Schedule()
    if call.data == "start":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите университет", reply_markup=get_universities_layout())
    if "select_university_" in call.data:
        university_id = call.data.split('select_university_')[1]
        bot.answer_callback_query(call.id, "Выбран университет \"" + schedule.name_by_id(university_id) + "\"")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите расписание (преподаватель/группа)",
                              reply_markup=get_types_layout(university_id))
        return
    if "select_type_" in call.data:
        selected_type = call.data.split('select_type_')[1].split('_')[0]
        university = call.data.split('university_')[1]
        translate = {'teacher': 'Преподаватель', 'student': 'Студент'}
        bot.answer_callback_query(call.id, "Выбран " + translate[selected_type])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите факультет",
                              reply_markup=get_faculties_layout(university, selected_type))
        return
    if "select_faculty_" in call.data:
        faculty = call.data.split('select_faculty_')[1].split('_')[0]
        selected_type = call.data.split('type_')[1].split('_')[0]
        university_id = call.data.split('university_')[1]
        bot.answer_callback_query(call.id, "Успешно выбрано")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите направление",
                              reply_markup=get_departments_layout(faculty, selected_type, university_id))
        return
    if "select_department_" in call.data:
        department = call.data.split('select_department_')[1].split('_')[0]
        selected_type = call.data.split('type_')[1].split('_')[0]
        faculty = call.data.split('faculty_')[1].split('_')[0]
        university = call.data.split('university_')[1]
        if selected_type == 'student':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Выберите группу",
                                  reply_markup=get_groups_layout(department, faculty, university))
        if selected_type == 'teacher':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Выберите преподавателя",
                                  reply_markup=get_teachers_layout(department, faculty, university))
        return
    if "select_group_" in call.data:
        group = call.data.split('select_group_')[1]
        current_date = datetime.today()

        text = pretty_date(current_date)
        lessons = schedule.get_group_schedule(group, current_date.strftime("%d.%m.%Y"))
        if not lessons:
            text += "\n\nПары отсутствуют"
        else:
            first = True
            for lesson in lessons:
                if first:
                    text += "\n👥 " + lesson['group'] + "\n"
                    first = False
                text += "\n⏱ " + lesson['classtime']['start'][:-3]
                text += "\n📚 " + lesson['type'] + ' ' + lesson['subject']
                text += "\n🚪 " + lesson['classroom']
                text += "\n👤 " + lesson['teacher']
                text += "\n⏱ " + lesson['classtime']['end'][:-3]
                text += "\n"
        bot.send_message(call.from_user.id, text, reply_markup=get_group_schedule_layout(group, current_date))
        return
    if "select_teacher_" in call.data:
        teacher = call.data.split('select_teacher_')[1]
        current_date = datetime.today()

        text = pretty_date(current_date)
        lessons = schedule.get_teacher_schedule(teacher, current_date.strftime("%d.%m.%Y"))
        if not lessons:
            text += "\n\nПары отсутствуют"
        else:
            first = True
            for lesson in lessons:
                if first:
                    text += "\n👥 " + lesson['teacher'] + "\n"
                    first = False
                text += "\n⏱ " + lesson['classtime']['start'][:-3]
                text += "\n📚 " + lesson['type'] + ' ' + lesson['subject']
                text += "\n🚪 " + lesson['classroom']
                text += "\n👤 " + lesson['group']
                text += "\n⏱ " + lesson['classtime']['end'][:-3]
                text += "\n"
        bot.send_message(call.from_user.id, text, reply_markup=get_teacher_schedule_layout(teacher, current_date))
        return
    if "schedule_group_" in call.data:
        group = call.data.split("schedule_group_")[1].split("_")[0]
        date = call.data.split("schedule_group_")[1].split("_")[1]

        current_date = datetime.strptime(date, '%d.%m.%Y')

        text = pretty_date(current_date)
        lessons = schedule.get_group_schedule(group, current_date.strftime("%d.%m.%Y"))
        if not lessons:
            text += "\n\nПары отсутствуют"
        else:
            first = True
            for lesson in lessons:
                if first:
                    text += "\n👥 " + lesson['group'] + "\n"
                    first = False
                text += "\n⏱ " + lesson['classtime']['start'][:-3]
                text += "\n📚 " + lesson['type'] + ' ' + lesson['subject']
                text += "\n🚪 " + lesson['classroom']
                text += "\n👤 " + lesson['teacher']
                text += "\n⏱ " + lesson['classtime']['end'][:-3]
                text += "\n"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,
                              reply_markup=get_group_schedule_layout(group, current_date))
        return
    if "schedule_teacher_" in call.data:
        teacher = call.data.split("schedule_teacher_")[1].split("_")[0]
        date = call.data.split("schedule_teacher_")[1].split("_")[1]

        current_date = datetime.strptime(date, '%d.%m.%Y')

        text = pretty_date(current_date)
        lessons = schedule.get_teacher_schedule(teacher, current_date.strftime("%d.%m.%Y"))
        if not lessons:
            text += "\n\nПары отсутствуют"
        else:
            first = True
            for lesson in lessons:
                if first:
                    text += "\n👥 " + lesson['teacher'] + "\n"
                    first = False
                text += "\n⏱ " + lesson['classtime']['start'][:-3]
                text += "\n📚 " + lesson['type'] + ' ' + lesson['subject']
                text += "\n🚪 " + lesson['classroom']
                text += "\n👤 " + lesson['group']
                text += "\n⏱ " + lesson['classtime']['end'][:-3]
                text += "\n"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,
                              reply_markup=get_teacher_schedule_layout(teacher, current_date))
        return


def pretty_date(date):
    russian_days = [
        'понедельник',
        'вторник',
        'среда',
        'четверг',
        'пятница',
        'суббота',
        'воскресенье',
    ]

    russian_months = [
        'января',
        'февраля',
        'марта',
        'апреля',
        'мая',
        'июня',
        'июля',
        'августа',
        'сентября',
        'октября',
        'ноября',
        'декабря'
    ]

    return '📆 ' + str(date.day) + ' ' + russian_months[date.month - 1] + ' (' + russian_days[date.weekday()] + ')'


def get_types_layout(university_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton('Студент', callback_data="select_type_student_university_" + str(university_id)),
        InlineKeyboardButton('Преподаватель', callback_data="select_type_teacher_university_" + str(university_id)),
        InlineKeyboardButton('<< Назад', callback_data="start"),
    )
    return markup


def get_teachers_layout(department, faculty, university):
    schedule = Schedule(department_id=department)
    markup = InlineKeyboardMarkup()
    markup.row_width = 3

    teachers = schedule.get_department_teachers()
    if len(teachers) == 0:
        markup.add(InlineKeyboardButton('Преподаватели отсутствуют', callback_data="none"))
    else:
        for i in range(0, len(teachers), 3):
            temp = []
            try:
                temp.append(InlineKeyboardButton(teachers[i]['short_name'], callback_data="select_teacher_" + str(
                    teachers[i]['id'])))
                temp.append(InlineKeyboardButton(teachers[i + 1]['short_name'], callback_data="select_teacher_" + str(
                    teachers[i + 1]['id'])))
                temp.append(InlineKeyboardButton(teachers[i + 2]['short_name'], callback_data="select_teacher_" + str(
                    teachers[i + 2]['id'])))
            except:
                pass
            markup.add(*temp)
    markup.add(InlineKeyboardButton("<< Назад", callback_data="select_faculty_" + str(faculty) + "_type_teacher_university_" + str(university)))
    return markup


def get_groups_layout(department, faculty, university):
    schedule = Schedule(department_id=department)
    markup = InlineKeyboardMarkup()
    markup.row_width = 3

    groups = schedule.get_department_groups()
    if len(groups) == 0:
        markup.add(InlineKeyboardButton('Группы отсутствуют', callback_data="none"))
    else:
        for i in range(0, len(groups), 3):
            temp = []
            try:
                temp.append(InlineKeyboardButton(groups[i]['short_name'], callback_data="select_group_" + str(
                    groups[i]['id'])))
                temp.append(InlineKeyboardButton(groups[i + 1]['short_name'], callback_data="select_group_" + str(
                    groups[i + 1]['id'])))
                temp.append(InlineKeyboardButton(groups[i + 2]['short_name'], callback_data="select_group_" + str(
                    groups[i + 2]['id'])))
            except:
                pass
            markup.add(*temp)

    markup.add(InlineKeyboardButton("<< Назад", callback_data="select_faculty_" + str(faculty) + "_type_student_university_" + str(university)))
    return markup


def get_group_schedule_layout(group_id, date):
    markup = InlineKeyboardMarkup()
    markup.row_width = 3

    current_date = date
    yesterday = current_date - timedelta(days=1)
    tomorrow = current_date + timedelta(days=1)

    markup.add(
        InlineKeyboardButton('<<', callback_data='schedule_group_' + str(group_id) + '_' + yesterday.strftime('%d.%m.%Y')),
        InlineKeyboardButton(current_date.strftime('%d.%m.%Y'), callback_data='schedule_group_' + str(group_id) + '_' + current_date.strftime('%d.%m.%Y')),
        InlineKeyboardButton('>>', callback_data='schedule_group_' + str(group_id) + '_' + tomorrow.strftime('%d.%m.%Y'))
    )

    minus_week = date - timedelta(days=7)
    plus_week = date + timedelta(days=7)
    markup.add(
        InlineKeyboardButton('<< Неделя', callback_data='schedule_group_' + str(group_id) + '_' + minus_week.strftime('%d.%m.%Y')),
        InlineKeyboardButton('Сброс даты', callback_data='schedule_group_' + str(group_id) + '_' + datetime.today().strftime('%d.%m.%Y')),
        InlineKeyboardButton('Неделя >>', callback_data='schedule_group_' + str(group_id) + '_' + plus_week.strftime('%d.%m.%Y'))
    )
    return markup


def get_teacher_schedule_layout(teacher_id, date):
    markup = InlineKeyboardMarkup()
    markup.row_width = 3

    current_date = date
    yesterday = current_date - timedelta(days=1)
    tomorrow = current_date + timedelta(days=1)

    markup.add(
        InlineKeyboardButton('<<', callback_data='schedule_teacher_' + str(teacher_id) + '_' + yesterday.strftime('%d.%m.%Y')),
        InlineKeyboardButton(current_date.strftime('%d.%m.%Y'), callback_data='schedule_teacher_' + str(teacher_id) + '_' + current_date.strftime('%d.%m.%Y')),
        InlineKeyboardButton('>>', callback_data='schedule_teacher_' + str(teacher_id) + '_' + tomorrow.strftime('%d.%m.%Y'))
    )

    minus_week = date - timedelta(days=7)
    plus_week = date + timedelta(days=7)
    markup.add(
        InlineKeyboardButton('<< Неделя', callback_data='schedule_teacher_' + str(teacher_id) + '_' + minus_week.strftime('%d.%m.%Y')),
        InlineKeyboardButton('Сброс даты', callback_data='schedule_teacher_' + str(teacher_id) + '_' + datetime.today().strftime('%d.%m.%Y')),
        InlineKeyboardButton('Неделя >>', callback_data='schedule_teacher_' + str(teacher_id) + '_' + plus_week.strftime('%d.%m.%Y'))
    )
    return markup


def get_universities_layout():
    schedule = Schedule()
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for university in schedule.universities():
        markup.add(
            InlineKeyboardButton(university['short_name'], callback_data="select_university_" + str(university['id'])))
    return markup


def get_faculties_layout(university_id, selected_type):
    schedule = Schedule(university_id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    faculties = schedule.get_university_faculties()
    for i in range(0, len(faculties), 2):
        temp = []
        try:
            temp.append(InlineKeyboardButton(faculties[i]['short_name'], callback_data="select_faculty_" + str(
                faculties[i]['id']) + "_type_" + selected_type + "_university_" + university_id))
            temp.append(InlineKeyboardButton(faculties[i + 1]['short_name'], callback_data="select_faculty_" + str(
                faculties[i + 1]['id']) + "_type_" + selected_type + "_university_" + university_id))
        except:
            pass
        markup.add(*temp)
    markup.add(InlineKeyboardButton("<< Назад", callback_data="select_university_" + university_id))
    return markup


def get_departments_layout(faculty_id, selected_type, university_id):
    schedule = Schedule(faculty_id=faculty_id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    departments = schedule.get_faculty_departments()
    for i in range(0, len(departments), 2):
        temp = []
        try:
            temp.append(InlineKeyboardButton(departments[i]['short_name'], callback_data="select_department_" + str(
                departments[i]['id']) + "_type_" + selected_type + "_faculty_" + str(faculty_id) + '_university_' + str(university_id)))
            temp.append(InlineKeyboardButton(departments[i + 1]['short_name'], callback_data="select_department_" + str(
                departments[i + 1]['id']) + "_type_" + selected_type + "_faculty_" + str(faculty_id) + '_university_' + str(university_id)))
        except:
            pass
        markup.add(*temp)

    markup.add(InlineKeyboardButton("<< Назад", callback_data="select_type_" + selected_type + "_university_" + university_id))
    return markup


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Выберите университет", reply_markup=get_universities_layout())


bot.polling(timeout=99999)
