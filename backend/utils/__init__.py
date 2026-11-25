def parse_unique_tags(raw: str) -> list[str]:
    return (
        sorted(list(set([tag.strip() for tag in raw.split(",") if tag.strip()])))
        if raw
        else []
    )
