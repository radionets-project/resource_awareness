from pygments.style import Style
from pygments.token import (
    Keyword,
    Name,
    Comment,
    String,
    Error,
    Literal,
    Number,
    Operator,
    Other,
    Punctuation,
    Text,
    Generic,
    Whitespace,
)

__all__ = ["CodeStyle", "CodeStyleLight"]

DARK_COLORS = dict(
    background="#222436",
    foreground="#f2f2f2",
    selection="#d6d6d7",
    comment="#adacaf",
    cyan="#00d7e9",
    green="#56f576",
    orange="#ffb183",
    pink="#ff508c",
    purple="#817ad4",
    red="#ff3a52",
    yellow="#ffe648",
    deletion="#8f0035",
)

LIGHT_COLORS = dict(
    background="#f2f2f2",
    foreground="#222436",
    selection="#515160",
    comment="#615f63",
    cyan="#00d7e9",
    green="#1fdb44",
    orange="#e67939",
    pink="#ff508c",
    purple="#5047b5",
    red="#d9142b",
    yellow="#d9ae11",
    deletion="#8f0035",
)


class CodeStyle(Style):
    """
    Custom code style for beamerthemecode.
    """

    name = "code"

    foreground_color = DARK_COLORS["foreground"]
    background_color = DARK_COLORS["background"]
    highlight_color = DARK_COLORS["selection"]
    line_number_color = DARK_COLORS["yellow"]
    line_number_background_color = DARK_COLORS["selection"]
    line_number_special_color = DARK_COLORS["green"]
    line_number_special_background_color = DARK_COLORS["comment"]

    styles = {
        Whitespace: DARK_COLORS["foreground"],
        Comment: DARK_COLORS["comment"],
        Comment.Preproc: DARK_COLORS["pink"],
        Generic: DARK_COLORS["foreground"],
        Generic.Deleted: DARK_COLORS["deletion"],
        Generic.Emph: "underline " + DARK_COLORS["foreground"],
        Generic.Heading: "bold " + DARK_COLORS["foreground"],
        Generic.Inserted: "bold " + DARK_COLORS["foreground"],
        Generic.Output: DARK_COLORS["selection"],
        Generic.EmphStrong: "underline " + DARK_COLORS["foreground"],
        Generic.Subheading: "bold " + DARK_COLORS["foreground"],
        Generic.Prompt: "bold " + DARK_COLORS["pink"],
        Error: DARK_COLORS["foreground"],
        Keyword: DARK_COLORS["pink"],
        Keyword.Constant: DARK_COLORS["pink"],
        Keyword.Declaration: "italic " + DARK_COLORS["green"],
        Keyword.Type: DARK_COLORS["green"],
        Literal: DARK_COLORS["foreground"],
        Name: DARK_COLORS["foreground"],
        Name.Attribute: DARK_COLORS["cyan"],
        Name.Builtin: "italic " + DARK_COLORS["green"],
        Name.Builtin.Pseudo: DARK_COLORS["yellow"],
        Name.Class: DARK_COLORS["cyan"],
        Name.Function: " bold " + DARK_COLORS["cyan"],
        Name.Label: "italic " + DARK_COLORS["green"],
        Name.Tag: DARK_COLORS["pink"],
        Name.Variable: "italic " + DARK_COLORS["green"],
        Number: DARK_COLORS["orange"],
        Operator: DARK_COLORS["pink"],
        Other: DARK_COLORS["foreground"],
        Punctuation: DARK_COLORS["foreground"],
        String: DARK_COLORS["yellow"],
        Text: DARK_COLORS["foreground"],
    }


class CodeStyleLight(Style):
    """
    Custom light code style for beamerthemecode.
    """

    name = "code-light"

    foreground_color = LIGHT_COLORS["foreground"]
    background_color = LIGHT_COLORS["background"]
    highlight_color = LIGHT_COLORS["selection"]
    line_number_color = LIGHT_COLORS["yellow"]
    line_number_background_color = LIGHT_COLORS["selection"]
    line_number_special_color = LIGHT_COLORS["green"]
    line_number_special_background_color = LIGHT_COLORS["comment"]

    styles = {
        Whitespace: LIGHT_COLORS["foreground"],
        Comment: LIGHT_COLORS["comment"],
        Comment.Preproc: LIGHT_COLORS["pink"],
        Generic: LIGHT_COLORS["foreground"],
        Generic.Deleted: LIGHT_COLORS["deletion"],
        Generic.Emph: "underline " + LIGHT_COLORS["foreground"],
        Generic.Heading: "bold " + LIGHT_COLORS["foreground"],
        Generic.Inserted: "bold " + LIGHT_COLORS["foreground"],
        Generic.Output: LIGHT_COLORS["selection"],
        Generic.EmphStrong: "underline " + LIGHT_COLORS["foreground"],
        Generic.Subheading: "bold " + LIGHT_COLORS["foreground"],
        Generic.Prompt: "bold " + LIGHT_COLORS["pink"],
        Error: LIGHT_COLORS["foreground"],
        Keyword: LIGHT_COLORS["pink"],
        Keyword.Constant: LIGHT_COLORS["pink"],
        Keyword.Declaration: "italic " + LIGHT_COLORS["green"],
        Keyword.Type: LIGHT_COLORS["green"],
        Literal: LIGHT_COLORS["foreground"],
        Name: LIGHT_COLORS["foreground"],
        Name.Attribute: LIGHT_COLORS["cyan"],
        Name.Builtin: "italic " + LIGHT_COLORS["green"],
        Name.Builtin.Pseudo: LIGHT_COLORS["yellow"],
        Name.Class: LIGHT_COLORS["cyan"],
        Name.Function: " bold " + LIGHT_COLORS["cyan"],
        Name.Label: "italic " + LIGHT_COLORS["green"],
        Name.Tag: LIGHT_COLORS["pink"],
        Name.Variable: "italic " + LIGHT_COLORS["green"],
        Number: LIGHT_COLORS["orange"],
        Operator: LIGHT_COLORS["pink"],
        Other: LIGHT_COLORS["foreground"],
        Punctuation: LIGHT_COLORS["foreground"],
        String: LIGHT_COLORS["yellow"],
        Text: LIGHT_COLORS["foreground"],
    }
