from datetime import datetime, timedelta

from typing import Generator

CHAT_PATH = 'chats.txt'
DATA_PATH = 'data.txt'

MAX_CHAT_INTERVAL = timedelta(hours = 1)
MIN_CHAT_MESSAGES = 10

def get_datetime(message: str) -> datetime:
	if not ',' in message or not '/' in message or not 'M' in message:
		return None

	# 10/4/21, 4:17 PM
	return datetime.strptime(message[:message.index('M') + 1], '%m/%d/%y, %I:%M %p')

def get_chat_threads(file_path: str = CHAT_PATH,
                     max_chat_interval: timedelta = MAX_CHAT_INTERVAL,
                     min_chat_messages: int = MIN_CHAT_MESSAGES) -> Generator[list[str], None, None]:
	with open(file_path, 'r', encoding='utf-8') as messages:
		thread = list()

		for message in messages:
			timestamp = get_datetime(message)
			if not timestamp:
				thread.append(message.strip())
				continue

			if len(thread) == 0 or timestamp - previous_timestamp <= max_chat_interval:
				thread.append(message.strip())
				previous_timestamp = timestamp
			else:
				if len(thread) >= min_chat_messages:
					yield thread

				thread = list()

	if len(thread) >= min_chat_messages:
		yield thread

def print_thread_durations(threads: Generator[list[str], None, None],
                           file_path: str = DATA_PATH):
	with open(file_path, 'w') as f:
		for thread in threads:
			f.write(f'{get_datetime(thread[0])}\t{get_datetime(thread[-1])}\t{len(thread)}\n')

def _run():
	threads = get_chat_threads()
	print_thread_durations(threads)


if __name__ == '__main__':
	_run()