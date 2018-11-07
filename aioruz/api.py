import os
import re
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from typing import Union, Any, List

import aiohttp
import pytz

CAMPUS_TIMEZONES = {
    'М': 'Europe/Moscow',
    'СПБ': 'Europe/Moscow',
    'НН': 'Europe/Moscow',
    'П': 'Asia/Yekaterinburg'
}


@dataclass
class Lesson(object):
    auditorium: str
    auditoriumAmount: int
    auditoriumOid: int
    author: str
    beginLesson: str
    building: str
    createddate: str
    date: str
    dateOfNest: str
    dayOfWeek: int
    dayOfWeekString: str
    detailInfo: str
    discipline: str
    disciplineOid: int
    disciplineinplan: str
    disciplinetypeload: int
    endLesson: str
    group: Any
    groupOid: int
    hideincapacity: int
    isBan: bool
    kindOfWork: str
    lecturer: str
    lecturerOid: int
    lessonNumberEnd: int
    lessonNumberStart: int
    modifieddate: str
    parentschedule: str
    stream: str
    streamOid: int
    subGroup: Any
    subGroupOid: int

    def __get_datetime_with_tz(self,
                               date: str,
                               time: str) -> datetime:
        tz_name = CAMPUS_TIMEZONES[self.campus]
        dt = datetime.strptime(
            'T'.join((date, time)),
            '%Y.%m.%dT%H:%M'
        )
        dt_loc = pytz.timezone(tz_name).localize(dt, is_dst=True)
        return dt_loc

    @property
    def auditorium_index(self) -> str:
        return self.auditorium.split('/')[-1]

    @property
    def campus(self) -> str:
        return self.auditorium.split(' ')[0]

    @property
    def starts_at(self) -> datetime:
        return self.__get_datetime_with_tz(self.date, self.beginLesson)

    @property
    def ends_at(self) -> datetime:
        return self.__get_datetime_with_tz(self.date, self.endLesson)

    @property
    def modified_at(self):
        iso_str = '+'.join(self.modifieddate.split('Z'))
        dt = datetime.fromisoformat(iso_str)
        return dt


BASE_URL = 'http://ruz.hse.ru/api'
ALLOWED_PERSON_TYPES = ('student', 'lecturer')

# Endpoints
SCHEDULE_ENDPOINT = 'schedule'
STUDENT_INFO_ENDPOINT = 'studentinfo'
SEARCH_INDPOINT = 'search'

HSE_EMAIL_SCHEMA = re.compile(r"^[a-z0-9._-]{3,}@(edu\.)?hse\.ru$")
VERIFY_SSL = os.environ.get('RUZ_VERIFY_SSL', False)


def is_hse_email(email: str) -> bool:
    return bool(HSE_EMAIL_SCHEMA.fullmatch(email.lower()))


def is_student_email(email: str) -> bool:
    return bool(HSE_EMAIL_SCHEMA.fullmatch(email.lower()).groups()[0])


def person_type_from_email(email: str) -> str:
    if is_student_email(email):
        return 'student'
    return 'lecturer'


def _date_to_ruz_date(d: date) -> str:
    return d.strftime('%Y.%m.%d')


async def api_request(url: str, params: dict):
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=VERIFY_SSL)) as session:
        async with session.get(url, params=params) as r:
            j = await r.json()
            if 'error' in j:
                raise LookupError('Bad Request')
            return j


async def search(q: str, person_type: str = 'student') -> list:
    """
    Search by query.
    :param q: `str` query to search for
    :param person_type: 'student', 'lecturer', 'group', 'auditorium'
    :return: list of results
    """
    url = '/'.join((BASE_URL, SEARCH_INDPOINT))
    params = {'term': q,
              'type': person_type}
    return await api_request(url, params)


async def student_info(email: str) -> dict:
    """
    Get student info
    :param email: `str` of student
    :return: `dict` with keys ('id', 'uns', 'email', 'fio', 'info')
    """
    url = '/'.join((BASE_URL, STUDENT_INFO_ENDPOINT))
    params = {'email': email}
    return await api_request(url, params)


async def schedule(person_type: str,
                   person_id: int,
                   from_date: date = None,
                   to_date: Union[date, int] = None,
                   language: int = 1) -> List[Lesson]:
    """
    Get schedule for users with specified person_type and person_id.
    :param person_type: 'student' or 'lecturer'
    :param person_id: RUZ ID of person
    :param from_date: `datetime.date` object (default `date.today()`)
    :param to_date: `datetime.date` object (default from_date + timedelta(7))
    :param language: `int` (default 1)
     1 for Russian
     2 for English
    :return: `List[Lesson]`
    """
    if person_type not in ALLOWED_PERSON_TYPES:
        raise ValueError(f'\'person_type\' must be one of {ALLOWED_PERSON_TYPES}, got {person_type} instead.')

    if from_date is None:
        from_date = date.today()
    if to_date is None:
        to_date = from_date + timedelta(days=7)
    elif isinstance(to_date, int):
        to_date = from_date + timedelta(days=to_date)

    url = '/'.join((BASE_URL, SCHEDULE_ENDPOINT, person_type, str(person_id)))
    params = {'lng': language, 'start': _date_to_ruz_date(from_date), 'finish': _date_to_ruz_date(to_date)}

    j = api_request(url, params)
    res = list()
    for lesson in await j:
        res.append(Lesson(**lesson))
    return res


async def student_schedule(email: str,
                           from_date: date = None,
                           to_date: date = None,
                           language: int = 1) -> list:
    """
    Get schedule for student based on his/her HSE email.
    :param email: `str`, email of student to get schedule with
    :param from_date: `datetime.date` object (default `date.today()`)
    :param to_date: `datetime.date` object (default from_date + timedelta(7))
    :param language: `int` (default 1)
    :return: `list` of lessons
    """
    info = await student_info(email=email)
    return await schedule(person_type='student',
                          person_id=int(info.get('id')),
                          from_date=from_date,
                          to_date=to_date,
                          language=language)
