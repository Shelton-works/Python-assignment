from datetime import datetime

def find_peak_usage(logs):
    counts = [0] * 24
    
    for log in logs:
        dt = datetime.fromisoformat(log)
        hour = dt.hour
        counts[hour] = counts[hour] + 1
        
    max_logins = max(counts)
    return counts.index(max_logins)

logs = [
    "2026-08-04T08:15:20",
    "2026-08-04T09:30:11",
    "2026-08-04T13:05:44",
    "2026-08-04T13:21:18",
    "2026-08-04T13:55:01",
    "2026-08-04T14:10:00"
]

print(find_peak_usage(logs))
