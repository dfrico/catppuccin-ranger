# This file is part of ranger, the console file manager.
# Available at https://github.com/ranger/ranger
# License: GNU GPL version 3, see the file "AUTHORS" for details.
# This theme was greatly inspired by "Dracula" for ranger
# It can be found in: `https://github.com/dracula/ranger`

from ranger.gui.colorscheme import ColorScheme
from ranger.gui.color import (
    default_colors, reverse, bold, normal, default
)

#
# Approximate xterm indices for Catppuccin Latte
# https://catppuccin.com/palette
# See hex2xterm.py
#
ROSEWATER    = 174  # ~ #DC8A78
FLAMINGO     = 174  # ~ #DD7878
PINK         = 176  # ~ #EA76CB
MAUVE        = 99   # ~ #8839EF
RED          = 161  # ~ #D20F39
MAROON       = 167  # ~ #E64553
PEACH        = 202  # ~ #FE640B
YELLOW       = 172  # ~ #DF8E1D
GREEN        = 70   # ~ #40A02B
TEAL         = 30   # ~ #179299
SKY          = 38   # ~ #04A5E5
SAPPHIRE     = 37   # ~ #209FB5
BLUE         = 27   # ~ #1E66F5
LAVENDER     = 69   # ~ #7287FD
TEXT         = 59   # ~ #4C4F69
SUBTEXT 1    = 60   # ~ #5C5F77
SUBTEXT 0    = 60   # ~ #6C6F85
OVERLAY 2    = 102  # ~ #7C7F93
OVERLAY 1    = 103  # ~ #8C8FA1
OVERLAY 0    = 145  # ~ #9CA0B0
SURFACE 2    = 145  # ~ #ACB0BE
SURFACE 1    = 146  # ~ #BCC0CC
SURFACE 0    = 188  # ~ #CCD0DA
BASE         = 231  # ~ #EFF1F5
MANTLE       = 189  # ~ #E6E9EF
CRUST        = 188  # ~ #DCE0E8

class CatppuccinLatte(ColorScheme):
    """
    A Catppuccin Latte color scheme for Ranger, approximated in 256 colors.
      - directories => bold, BLUE
      - documents => MAUVE
      - media => image=YELLOW, video=RED, audio=TEAL, else=GREEN
      - containers => MAROON
      - link => TEAL (good) or MAUVE (bad)
      - socket => PINK
      - etc.
    """
    progress_bar_color = BLUE

    def verify_browser(self, context, fg, bg, attr):
        if context.selected:
            # attr = reverse
            bg = SURFACE_0
            fg = BASE
            attr &= ~bold
        else:
            attr = normal

        if context.empty or context.error:
            bg = RED
            fg = BASE

        if context.border:
            fg = OVERLAY_2

        if context.document:
            attr |= normal
            fg = MAUVE

        # Media detection => image, video, audio, else
        if context.media:
            if context.image:
                attr |= normal
                fg = YELLOW
            elif context.video:
                fg = RED
            elif context.audio:
                fg = TEAL
            else:
                fg = GREEN  # e.g., .bin, .iso, etc.

        if context.container:
            # e.g. .tar, .zip, etc.
            attr |= bold
            fg = MAROON

        if context.directory:
            attr |= bold
            fg = SAPPHIRE

        elif context.executable and not any(
            (context.media, context.container, context.fifo, context.socket)
        ):
            attr |= bold
            fg = GREEN

        if context.socket:
            fg = PINK
            attr |= bold

        if context.fifo or context.device:
            fg = YELLOW
            if context.device:
                attr |= bold

        if context.link:
            # Good link => TEAL, bad => MAUVE
            fg = TEAL if context.good else MAUVE

        # Tag marker => bold highlight
        if context.tag_marker and not context.selected:
            attr |= bold
            # We'll conditionally change color if it's red/magenta
            if fg in (RED, PINK, MAROON):
                fg = 15   # white
            else:
                fg = RED

        if not context.selected and (context.cut or context.copied):
            fg = GRAY
            attr |= bold

        # Main column markings
        if context.main_column:
            if context.selected:
                attr |= bold
            if context.marked:
                attr |= bold
                fg = YELLOW

        # Bad info
        if context.badinfo:
            if attr & reverse:
                bg = PINK
            else:
                fg = PINK

        if context.inactive_pane:
            fg = TEAL # or CYAN

        return fg, bg, attr

    def verify_titlebar(self, context, fg, bg, attr):
        attr |= bold
        if context.hostname:
            fg = RED if context.bad else GREEN
        elif context.directory:
            fg = BLUE
        elif context.tab:
            if context.good:
                bg = GREEN
        elif context.link:
            fg = TEAL

        return fg, bg, attr

    def verify_statusbar(self, context, fg, bg, attr):
        if context.permissions:
            if context.good:
                fg = GREEN
            elif context.bad:
                bg = PINK
                fg = GRAY

        if context.marked:
            attr |= bold | reverse
            fg = YELLOW

        if context.frozen:
            attr |= bold | reverse
            fg = TEAL

        if context.message:
            if context.bad:
                attr |= bold
                fg = RED

        if context.loaded:
            bg = self.progress_bar_color

        if context.vcsinfo:
            fg = BLUE
            attr &= ~bold

        if context.vcscommit:
            fg = YELLOW
            attr &= ~bold

        if context.vcsdate:
            fg = TEAL
            attr &= ~bold

        return fg, bg, attr

    def verify_taskview(self, context, fg, bg, attr):
        if context.title:
            fg = BLUE  # or TEAL

        if context.selected:
            attr |= reverse

        if context.loaded:
            if context.selected:
                fg = self.progress_bar_color
            else:
                bg = self.progress_bar_color

        return fg, bg, attr

    def verify_vcsfile(self, context, fg, bg, attr):
        attr &= ~bold

        if context.vcsconflict:
            fg = PINK
        elif context.vcschanged:
            fg = RED
        elif context.vcsunknown:
            fg = RED
        elif context.vcsstaged:
            fg = GREEN
        elif context.vcssync:
            fg = GREEN
        elif context.vcsignored:
            fg = default

        return fg, bg, attr

    def verify_vcsremote(self, context, fg, bg, attr):
        # Same pattern: remove bold, set color by VCS status
        attr &= ~bold

        if context.vcssync or context.vcsnone:
            fg = GREEN
        elif context.vcsbehind:
            fg = RED
        elif context.vcsahead:
            fg = TEAL
        elif context.vcsdiverged:
            fg = PINK
        elif context.vcsunknown:
            fg = RED

        return fg, bg, attr

    def use(self, context):
        fg, bg, attr = default_colors

        if context.reset:
            return default_colors

        elif context.in_browser:
            fg, bg, attr = self.verify_browser(context, fg, bg, attr)

        elif context.in_titlebar:
            fg, bg, attr = self.verify_titlebar(context, fg, bg, attr)

        elif context.in_statusbar:
            fg, bg, attr = self.verify_statusbar(context, fg, bg, attr)

        # Highlight text matches
        if context.text and context.highlight:
            attr |= reverse

        # Task view
        if context.in_taskview:
            fg, bg, attr = self.verify_taskview(context, fg, bg, attr)

        # VCS file or remote
        if context.vcsfile and not context.selected:
            fg, bg, attr = self.verify_vcsfile(context, fg, bg, attr)
        elif context.vcsremote and not context.selected:
            fg, bg, attr = self.verify_vcsremote(context, fg, bg, attr)

        return fg, bg, attr
