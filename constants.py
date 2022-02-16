import curses


stdscr = curses.initscr()


def color_initialize():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 88, 234)
    curses.init_pair(2, 51, 234)
    curses.init_pair(3, 5, 234)
    curses.init_pair(4, 208, 234)
    curses.init_pair(5, 4, 234)
    curses.init_pair(6, 14, 234)
    curses.init_pair(7, 2, 234)
    curses.init_pair(8, 27, 234)
    curses.init_pair(9, 244, 234)
    curses.init_pair(9, 0, 234)
    return (
        curses.color_pair(1),
        curses.color_pair(2),
        curses.color_pair(3),
        curses.color_pair(4),
        curses.color_pair(5),
        curses.color_pair(6),
        curses.color_pair(7),
        curses.color_pair(8),
        curses.color_pair(9),
        curses.color_pair(10),
    )


colors = color_initialize()
