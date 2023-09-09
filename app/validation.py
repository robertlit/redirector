import re
from typing import Tuple, Optional

import validators


def validate_request_body(data) -> Tuple[bool, Optional[str]]:
    if not isinstance(data, dict):
        return False, "Request body must be JSON object"

    fields = [
        ("src", str, validate_src, False),
        ("target", str, validate_target, True)
    ]

    for field_name, field_type, field_validate, required in fields:
        if field_name not in data:
            if required:
                return False, f"Missing {field_name}"

            continue

        if not isinstance(data[field_name], field_type):
            return False, f"Invalid type for {field_name}: {field_type.__name__} expected"

        is_valid_field, field_err_msg = field_validate(data[field_name])
        if not is_valid_field:
            return False, field_err_msg

    return True, None


def validate_src(src: str) -> Tuple[bool, Optional[str]]:
    pattern = r"^[A-Za-z0-9]{10}$"
    if not re.match(pattern, src):
        return False, "Source must be of length 10 and consist of letters and/or digits"

    return True, None


def validate_target(target: str) -> Tuple[bool, Optional[str]]:
    if not validators.url(target):
        return False, "Target must be a valid URL"

    return True, None
