from datetime import datetime, timedelta

def humanize_time_difference(time):
    now = datetime.now(time.tzinfo)
    diff = now - time

    if diff < timedelta(minutes=1):
        return "agora"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() // 60)
        return f"há {minutes} minuto{'s' if minutes != 1 else ''}"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() // 3600)
        return f"há {hours} hora{'s' if hours != 1 else ''}"
    elif diff < timedelta(days=2):
        return "ontem"
    elif diff < timedelta(days=7):
        days = diff.days
        return f"há {days} dia{'s' if days != 1 else ''}"
    else:
        return time.strftime('%d/%m/%Y')