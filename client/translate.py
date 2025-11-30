#  Copyright (c) 2025 Timofei Kirsanov

from client import settings


def get(key_f: str, placeholders: tuple = None):
    values = {}
    with open(f"langs/{settings.language}.lang", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            key, value = map(str, line.strip().split("=", maxsplit=1))
            values[key] = value

    if placeholders:
        result = list(values[key_f])
        is_placeholder = False
        i = 0
        placeholders_index = []
        for symbol in values[key_f]:
            if is_placeholder and symbol == "s":
                placeholders_index.append(i)
            if symbol == "%":
                is_placeholder = True
            else:
                is_placeholder = False
            i += 1
        for i in range(len(placeholders)):
            result[placeholders_index[i]] = ""
            result[placeholders_index[i] - 1] = placeholders[i]
            return "".join(result).replace('\\n', '\n')
    else:
        return values[key_f].replace('\\n', '\n')
