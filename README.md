# Async HSE RUZ API cleint for Python3
## Usage
To obtain student's schedule:

```python
from datetime import date, timedelta

import asyncio
import aioruz

async def main():
	print(await aioruz.student_schedule(email='example@hse.ru',
	 									from_date=date.today(),
	 									to_date=date.today+timedelta(days=7)))
	print(await aioruz.schedule(person_type='lecturer', 
								person_id=12345,
								from_date=date.))

loop = asyncio.get_event_loop()
lessos = 
```
## Installiation
Install via Pip:

```bash
pip install aioruz
```