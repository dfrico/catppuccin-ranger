import re
from pathlib import Path

from colors import COLORS
from hex2xterm import rgb2short

BASE_FILE = Path("base_config.py")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
PLACEHOLDER_PATTERN = r'^([A-Z0-9_]+)\s*=\s*".*?"'


def hex_to_xterm(value: str) -> str:
    """Converts a hex color code to an xterm color code.

    Args:
        value: A string representing a hex color code (e.g., '#FF0000' or 'FF0000').

    Returns:
        A string representing the corresponding xterm color code.

    Raises:
        ValueError: If the hex color code is invalid.
    """

    if not re.match(r"^#?[0-9A-Fa-f]{6}$", value):
        raise ValueError(f"Invalid hex color code: {value}")

    return rgb2short(value)[0]


def flavor_to_xterm(flavor: dict[str, str]) -> dict[str, str]:
    """Converts each hex color in a flavor to xterm color codes.

    Args:
        flavor: A dictionary mapping color names to hex color codes.

    Returns:
        A dictionary mapping color names to xterm color codes.
    """

    return {key.lower(): hex_to_xterm(value) for key, value in flavor.items()}


def get_base_config(input_path: Path = BASE_FILE) -> str:
    """Reads the base configuration file.

    Args:
        input_path: Path to the base configuration file.

    Returns:
        The contents of the file as a string.

    Raises:
        FileNotFoundError: If the input file does not exist.
        IOError: If there is an error reading the file.
    """

    input_path = BASE_FILE.resolve() if input_path == BASE_FILE else Path(input_path)

    try:
        return input_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Base config file not found: {input_path}")
    except IOError as e:
        raise IOError(f"Error reading {input_path}: {e}")


def save_new_config(
    contents: str, flavor_name: str, output_path: Path = OUTPUT_DIR
) -> None:
    """Writes a new configuration file for a given flavor.

    Args:
        contents: The configuration file contents.
        flavor_name: The name of the flavor (e.g., 'latte').
        output_path: The directory to save the output file.

    Raises:
        ValueError: If the flavor name is invalid.
        IOError: If there is an error writing the file.
    """

    try:
        flavor_key = flavor_name.split()[0].lower()
    except IndexError:
        raise ValueError(f"Invalid flavor name: {flavor_name}")

    flavor_key = re.sub(r"[^a-z0-9_]", "", flavor_key)
    output = output_path / f"catppuccin_{flavor_key}.py"
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        _ = output.write_text(contents, encoding="utf-8")
    except IOError as e:
        raise IOError(f"Error writing to {output}: {e}")


def update_config_colors(config: str, flavor: dict[str, str]) -> str:
    """Replaces placeholder color values in the config with xterm values.

    Args:
        config: The base configuration string.
        flavor: A dictionary mapping color names to xterm color codes.

    Returns:
        The updated configuration string with replaced color values.
    """
    pattern = re.compile(PLACEHOLDER_PATTERN, re.MULTILINE)

    def replacer(match: re.Match[str]) -> str:
        key = match.group(1)
        lower_key = key.lower()
        return f"{key} = {flavor.get(lower_key, match.group(0))!r}"

    return pattern.sub(replacer, config)


def update_config_classname(config: str, flavor_name: str) -> str:
    """Updates the class name in the config based on the flavor name.

    Args:
        config: The configuration string.
        flavor_name: The name of the flavor (e.g., 'latte').

    Returns:
        The configuration string with the updated class name.
    """
    try:
        name = flavor_name.split()[0].lower().capitalize()
    except IndexError:
        raise ValueError(f"Invalid flavor name: {flavor_name}")
    return config.replace("BaseConfig", f"Catppuccin{name}")


def update_config(config: str, flavor: dict[str, str], flavor_name: str) -> str:
    """Updates the config with xterm colors and a new class name.

    Args:
        config: The base configuration string.
        flavor: A dictionary mapping color names to xterm color codes.
        flavor_name: The name of the flavor (e.g., 'latte').

    Returns:
        The updated configuration string.
    """
    colors = update_config_colors(config, flavor)
    return update_config_classname(colors, flavor_name)


def create_palettes() -> None:
    """Generates configuration files for each flavor in COLORS."""
    base = get_base_config()
    required_keys = set(k.lower() for k in re.findall(PLACEHOLDER_PATTERN, base))

    for flavor_name, flavor in COLORS.items():
        missing_keys = required_keys - set(flavor.keys())

        if missing_keys:
            raise ValueError(
                f"Flavor {flavor_name} missing required colors: {missing_keys}"
            )

        flavor_xterm = flavor_to_xterm(flavor)
        config = update_config(base, flavor_xterm, flavor_name)
        save_new_config(config, flavor_name)

    return


if __name__ == "__main__":
    create_palettes()
