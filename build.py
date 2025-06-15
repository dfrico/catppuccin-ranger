import re
from pathlib import Path
from venv import create

from colors import COLORS
from hex2xterm import rgb2short

BASE_FILE = Path("base_config.py")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
PLACEHOLDER_PATTERN = r'^([A-Z_]+)\s*=\s*["\']\.\.\.["\']'


def hex_to_xterm(value: str) -> str:
    """Just wraps the hex2xterm function, converts a hex color to xterm"""

    return rgb2short(value)[0]


def flavor_to_xterm(flavor: dict[str, str]) -> dict[str, str]:
    """Convert each color in a flavor to xterm, returns a converted dict"""

    output: dict[str, str] = {}

    for key, value in flavor.items():
        output[key] = hex_to_xterm(value)

    return output


def get_base_config(input_path: str = "./base_config.py") -> str:
    """Gets the value of the "base_config.py" file, returns it as a string"""

    input = Path(input_path)
    contents = input.read_text(encoding="utf-8")

    return contents


def save_new_config(
    contents: str, flavor_name: str, output_path: str = "./output"
) -> None:
    """Writes the new config file to the specified directory"""

    output = Path(f"{output_path}/catppuccin_{flavor_name.split()[0].lower()}.py")
    output.parent.mkdir(parents=True, exist_ok=True)
    _ = output.write_text(contents, encoding="utf-8")

    return


def update_config_colors(config: str, flavor: dict[str, str]) -> str:
    replaced: set[str] = set()
    pattern = re.compile(r'^([A-Z0-9_]+)\s*=\s*".*?"', re.MULTILINE)

    def replacer(match: re.Match[str]) -> str:
        key = match.group(1)
        lower_key = key.lower()

        if lower_key in flavor and lower_key not in replaced:
            replaced.add(lower_key)
            return f"{key} = {flavor[lower_key]}"

        return match.group(0)

    return pattern.sub(replacer, config)


def update_config_classname(config: str, flavor_name: str) -> str:
    name = flavor_name.split()[0].lower().capitalize()
    updated = config.replace("BaseConfig", f"Catppuccin{name}")
    return updated


def update_config(config: str, flavor: dict[str, str], flavor_name: str) -> str:
    colors = update_config_colors(config, flavor)
    classname = update_config_classname(colors, flavor_name)

    return classname


def create_palettes() -> None:
    base = get_base_config()
    for flavor_name, flavor in COLORS.items():
        print(f"Converting {flavor_name.split()[0].lower().capitalize()}")
        flavor_xterm = flavor_to_xterm(flavor)
        config = update_config(base, flavor_xterm, flavor_name)

        save_new_config(config, flavor_name)

    return


create_palettes()
