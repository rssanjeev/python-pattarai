import requests
import datetime
from collections import defaultdict

# Constants
USER_KEY = "98ddfac749640524d2b6c2260811"
FETCH_URL = f"https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey={USER_KEY}"
TEST_FETCH_URL = "https://candidate.hubteam.com/candidateTest/v3/problem/test-dataset?userKey=98ddfac749640524d2b6c2260811"

def fetch_call_data():
    """Fetches call data from the given API endpoint."""
    response = requests.get(TEST_FETCH_URL)
    if response.status_code == 200:
        return response.json()["callRecords"]
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def timestamp_to_utc_date(timestamp):
    """Converts a UNIX timestamp (milliseconds) to a UTC date string (YYYY-MM-DD)."""
    return datetime.datetime.utcfromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")

def process_calls(calls):
    """
    Processes call records to determine the maximum concurrent calls per customer per day.
    Returns a structured result.
    """
    # Dictionary: {customerId -> {date -> list of (start, end, callId)}}
    customer_calls = defaultdict(lambda: defaultdict(list))

    # Track calls that span multiple days
    ongoing_calls = defaultdict(lambda: defaultdict(set))  # {customerId -> {date -> set(callIds)}}

    # Group calls by customer and day
    for call in calls:
        customer_id = call["customerId"]
        start = call["startTimestamp"]
        end = call["endTimestamp"]
        call_id = call["callId"]

        # Calls spanning multiple days
        current_day = timestamp_to_utc_date(start)
        
        while start < end:
            next_day = timestamp_to_utc_date(start + 86400000)  # Move to the next day
            day_end = min(end, int(datetime.datetime.strptime(next_day, "%Y-%m-%d").timestamp() * 1000))
            customer_calls[customer_id][current_day].append((start, day_end, call_id))

            # Fix: Ensure call is tracked for **all days it spans**, not just the last one
            if day_end < end:
                ongoing_calls[customer_id][next_day].add(call_id)

            # Move to next day
            start = day_end
            current_day = timestamp_to_utc_date(start)

    # Process concurrency for each customer and each day
    results = []
    
    for customer_id, days in customer_calls.items():
        active_ongoing_calls = set()  # Track ongoing calls from the previous day

        for date, call_list in sorted(days.items()):  # Process dates in order
            events = []
            
            # Fix: Ensure previous day's ongoing calls are counted **before sorting events**
            active_calls = set(active_ongoing_calls)  # Include ongoing calls from previous day
            
            # Add ongoing calls as "start" events at midnight (beginning of the day)
            for call_id in active_ongoing_calls:
                events.append((int(datetime.datetime.strptime(date, "%Y-%m-%d").timestamp() * 1000), 1, call_id))

            # Process current day's call events
            for start, end, call_id in call_list:
                events.append((start, 1, call_id))  # Call start
                events.append((end, -1, call_id))   # Call end

            # Sort by timestamp (breaking ties by processing start before end)
            events.sort()

            # Fix: Ensure concurrency starts with the ongoing calls
            max_concurrent = len(active_calls)
            max_timestamp = 0
            max_call_ids = set(active_calls)

            # Sweep line to determine peak concurrent calls
            for timestamp, event_type, call_id in events:
                if event_type == 1:  # Start of a call
                    active_calls.add(call_id)
                    if len(active_calls) > max_concurrent:
                        max_concurrent = len(active_calls)
                        max_timestamp = timestamp
                        max_call_ids = active_calls.copy()
                else:  # End of a call
                    active_calls.remove(call_id)

            # Store the result for this customer and date
            if max_concurrent > 0:
                results.append({
                    "customerId": customer_id,
                    "date": date,
                    "maxConcurrentCalls": max_concurrent,
                    "timestamp": max_timestamp,
                    "callIds": list(max_call_ids)
                })

            # Fix: Ensure only calls that continue into the next day are tracked
            active_ongoing_calls = ongoing_calls[customer_id][date].copy()
            ongoing_calls[customer_id][date].clear()  # Fix: Reset after copying to avoid retaining old calls

    return {"results": results}

def send_results(results):
    """Sends the computed results to the POST endpoint."""
    response = requests.post(POST_URL, json=results)
    if response.status_code == 200:
        print("Successfully sent results.")
    else:
        print(f"Failed to send results: {response.status_code}, {response.text}")

# Main Execution
if __name__ == "__main__":
    try:
        call_data = fetch_call_data()
        processed_results = process_calls(call_data)
        print(processed_results)
    except Exception as e:
        print(f"Error: {e}")
