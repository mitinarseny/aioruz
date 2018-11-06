# aioruz
[![PyPI version shields.io](https://img.shields.io/pypi/v/aioruz.svg)](https://pypi.org/project/aioruz/)
> Async HSE RUZ API client for Python 3.
## Usage
To obtain student's schedule:

```python
from datetime import date, timedelta

import asyncio
import aioruz


async def main():
    # Get schedule on 10 days forward
    print(await aioruz.student_schedule(email='example1@edu.hse.ru', to_date=10))  

    # Suitable for lecturers as there is no way to get lecturer's person_id by email
    print(await aioruz.schedule(person_type='lecturer',
                                person_id=12345,
                                from_date=date.today(),
                                to_date=date.today() + timedelta(days=7))

    # Get student's info by email
    print(await aioruz.student_info('example@edu.hse.ru'))

    # Search for query
    print(await aioruz.search('some name'))

loop = asyncio.get_event_loop()
loop.run_until_completed(main())
```
## Installiation
Install via Pip:

```bash
pip install aioruz
```

## Security
By default SSL certificate validation is off. To ebale it, set `RUZ_VERIFY_SSL` environment virable to `True`.
```python
import os

os.environ['RUZ_VERIFY_SSL'] = True
```
# Feedback
Please, send your bug reports to [this](https://t.me/joinchat/BpQR5w35HBg3CB1zJYlRHw) Telegram chat.
