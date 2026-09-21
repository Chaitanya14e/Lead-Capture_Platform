from slowapi import Limiter


def get_rate_limit_key(request):
    client_ip = request.client.host if request.client else "unknown"

    widget_id = request.query_params.get("widget_id")

    if not widget_id:
        return client_ip

    return f"{client_ip}:{widget_id}"


limiter = Limiter(
    key_func=get_rate_limit_key,
)