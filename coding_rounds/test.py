import requests
from datetime import datetime, timedelta
from collections import defaultdict


def get_dates_between(start_timestamp, end_timestamp):
    start_date = datetime.utcfromtimestamp(start_timestamp / 1000).date()
    end_date = datetime.utcfromtimestamp(end_timestamp / 1000).date()

    current_date = start_date
    dates = []

    while current_date <= end_date:
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)

    return dates

class PhoneRecords:
    def __init__(self, url):
        self.url = url
        self.records = self.__get_records()

    def __get_records(self):
        response = requests.get(self.url)
        return response.json()

    def __process_results(self, result):
        answer = {'results': []}

        for customer_id in result:
            for date in result[customer_id]:
                if result[customer_id][date]['maxConcurrentCalls'] > 0:  # Only include dates with calls
                    current_data = {
                        'customerId': customer_id,
                        'date': date,
                        'maxConcurrentCalls': result[customer_id][date]['maxConcurrentCalls'],
                        'callIds': result[customer_id][date]['callIds'],
                        'timestamp': result[customer_id][date]['timestamp']
                    }
                    answer['results'].append(current_data)

        return answer

    def get_peak_phone_calls(self):
        customer_concurrent_data_by_date = defaultdict(lambda: defaultdict(list))

        # Organize the records
        for record in self.records['callRecords']:
            customer_id = record['customerId']
            start_timestamp = record['startTimestamp']
            end_timestamp = record['endTimestamp'] - 1

            dates_active = get_dates_between(start_timestamp, end_timestamp)

            start_date = datetime.utcfromtimestamp(start_timestamp / 1000).strftime('%Y-%m-%d')
            end_date = datetime.utcfromtimestamp(end_timestamp / 1000).strftime('%Y-%m-%d')

            if start_date == end_date:
                # Call starts and ends on the same date
                customer_concurrent_data_by_date[customer_id][start_date].append(
                    (start_timestamp, 'start', record['callId']))
                customer_concurrent_data_by_date[customer_id][start_date].append(
                    (end_timestamp, 'end', record['callId']))

            else:
                customer_concurrent_data_by_date[customer_id][start_date].append(
                    (start_timestamp, 'start', record['callId'])
                )
                for date in dates_active[1:]:
                    customer_concurrent_data_by_date[customer_id][date].append(
                        (int(datetime.strptime(date, '%Y-%m-%d').timestamp() * 1000), 'start', record['callId'])
                    )
                customer_concurrent_data_by_date[customer_id][end_date].append(
                    (end_timestamp, 'end', record['callId'])
                )

        # Process each customer call data
        result = {}

        for customer_id, date_events in customer_concurrent_data_by_date.items():
            result[customer_id] = {}

            for date, events in date_events.items():
                # Sort events by timestamp and event type
                events.sort(key=lambda x: (x[0], x[1] == 'start'))
                print(events)

                concurrent_calls = 0
                max_concurrent_calls = 0
                max_timestamp = None
                active_calls = set()
                call_ids_at_max_concurrency = []

                # Parse through the events to count concurrent calls for a date
                for timestamp, event_type, call_id in events:
                    if event_type == 'start':
                        concurrent_calls += 1
                        active_calls.add(call_id)
                        if concurrent_calls >= max_concurrent_calls:
                            max_concurrent_calls = concurrent_calls
                            max_timestamp = timestamp
                            call_ids_at_max_concurrency = list(active_calls)
                    else:
                        if call_id in active_calls:
                            concurrent_calls -= 1
                            active_calls.remove(call_id)

                result[customer_id][date] = {
                    'maxConcurrentCalls': max_concurrent_calls,
                    'callIds': call_ids_at_max_concurrency,
                    'timestamp': max_timestamp
                }

        return self.__process_results(result)

    def send_records(self, url):
        payload = self.get_peak_phone_calls()
        print(payload)  # For debugging, to see what will be sent
        response = requests.post(url, json=payload)
        print(f"Response Status Code: {response.status_code}")


if __name__ == '__main__':
    phone_records = PhoneRecords(
        'https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=98ddfac749640524d2b6c2260811'
    )

    phone_records.send_records(
        'https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey=98ddfac749640524d2b6c2260811'
    )