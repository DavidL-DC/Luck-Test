from collections.abc import Callable

import customtkinter as ctk

from games import COIN_TOSS_COUNT, CoinSide, CoinTossGame, GameResult
from scoring import calculate_luck_score, get_result_message


APP_TITLE = "Luck Meter"
WINDOW_SIZE = "420x420"
WINDOW_MIN_SIZE = 420
SCREEN_PADDING_X = 40
DEFAULT_SCREEN_PADDING_Y = 40
RESULT_SCREEN_PADDING_Y = 36
SPACING_TINY = 4
SPACING_SMALL = 8
SPACING_MEDIUM = 16
SPACING_LARGE = 28
CONTENT_WIDTH = 320
TOSS_REVEAL_DELAY_MS = 180
TOSS_COLUMNS = 5
BUTTON_CORNER_RADIUS = 8
PRIMARY_BUTTON_WIDTH = 180
PRIMARY_BUTTON_HEIGHT = 40
START_BUTTON_HEIGHT = 44
CHOICE_BUTTON_WIDTH = 140
CHOICE_BUTTON_HEIGHT = 48
TOSS_LABEL_WIDTH = 46
TOSS_LABEL_HEIGHT = 34
TITLE_FONT_SIZE = 36
GAME_TITLE_FONT_SIZE = 24
RESULT_TITLE_FONT_SIZE = 28
BODY_FONT_SIZE = 14
BUTTON_FONT_SIZE = 14
RESULT_MESSAGE_FONT_SIZE = 15
SCORE_FONT_SIZE = 30


class Texts:
    APP_TITLE = "Luck Meter"
    START_SUBTITLE = "Teste dein Glück in kurzen Mini-Spielen."
    START_BUTTON = "Start"
    GAME_TITLE = "Münzwurf-Serie"
    GAME_SUBTITLE = "Wähle eine Seite. Danach fallen 10 Münzen."
    HEADS_BUTTON = "Kopf"
    TAILS_BUTTON = "Zahl"
    TOSS_PLACEHOLDER = "Bereit"
    TOSS_UNKNOWN = "?"
    RESULT_TITLE = "Ergebnis"
    POINTS_LABEL = "Punkte"
    LUCK_SCORE_LABEL = "Vorläufiger Luck Score"
    SELECTED_SIDE_STATUS = "Gewählt: {side}"
    HITS_DETAIL = "{hits} von {total_rounds} Treffern"
    PERCENT_VALUE = "{score:.1f}%"
    LUCK_SCORE_VALUE = "{score:.1f}/10"
    RESTART_BUTTON = "Nochmal"
    HOME_BUTTON = "Startscreen"


class Colors:
    BACKGROUND = "#111318"
    SURFACE = "#1a1f29"
    SURFACE_LIGHT = "#242933"
    SURFACE_HOVER = "#303743"
    PRIMARY = "#2f7df6"
    PRIMARY_HOVER = "#2567ca"
    TEXT = "#f4f7fb"
    TEXT_MUTED = "#a8b0bd"
    TEXT_DIM = "#657082"
    WHITE = "#ffffff"


class LuckMeterApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(WINDOW_MIN_SIZE, WINDOW_MIN_SIZE)
        self.maxsize(WINDOW_MIN_SIZE, WINDOW_MIN_SIZE)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self._active_frame: ctk.CTkFrame | None = None
        self._coin_game = CoinTossGame()
        self.configure(fg_color=Colors.BACKGROUND)

    def show_start_screen(self) -> None:
        self._set_screen(StartScreen(self, on_start=self.show_coin_toss_screen))

    def show_coin_toss_screen(self) -> None:
        self._set_screen(CoinTossScreen(self, on_result=self.show_result_screen))

    def show_result_screen(self, result: GameResult) -> None:
        screen = ResultScreen(
            self,
            result=result,
            on_restart=self.show_coin_toss_screen,
            on_home=self.show_start_screen,
        )
        self._set_screen(screen)

    def play_coin_toss(self, selected_side: CoinSide) -> GameResult:
        return self._coin_game.play(selected_side)

    def _set_screen(self, frame: ctk.CTkFrame) -> None:
        if self._active_frame is not None:
            self._active_frame.destroy()

        self._active_frame = frame
        self._active_frame.pack(fill="both", expand=True)


class BaseScreen(ctk.CTkFrame):
    def __init__(self, master: LuckMeterApp) -> None:
        super().__init__(master, fg_color=Colors.BACKGROUND, corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


class StartScreen(BaseScreen):
    def __init__(self, master: LuckMeterApp, on_start: Callable[[], None]) -> None:
        super().__init__(master)
        self._on_start = on_start
        self._build()

    def _build(self) -> None:
        content = create_content_frame(self)

        title = create_title(content, Texts.APP_TITLE, size=TITLE_FONT_SIZE)
        title.pack(pady=(0, SPACING_SMALL))

        subtitle = create_body_label(content, Texts.START_SUBTITLE)
        subtitle.pack(pady=(0, SPACING_LARGE))

        start_button = create_primary_button(
            content,
            Texts.START_BUTTON,
            self._on_start,
            width=PRIMARY_BUTTON_WIDTH,
            height=START_BUTTON_HEIGHT,
        )
        start_button.pack()


class CoinTossScreen(BaseScreen):
    def __init__(
        self,
        master: LuckMeterApp,
        on_result: Callable[[GameResult], None],
    ) -> None:
        super().__init__(master)
        self._on_result = on_result
        self._result: GameResult | None = None
        self._revealed_tosses = 0
        self._choice_buttons: list[ctk.CTkButton] = []
        self._toss_labels: list[ctk.CTkLabel] = []
        self._status_label: ctk.CTkLabel | None = None
        self._build()

    def _build(self) -> None:
        content = create_content_frame(self)

        title = create_title(content, Texts.GAME_TITLE, size=GAME_TITLE_FONT_SIZE)
        title.pack(pady=(0, SPACING_SMALL))

        subtitle = create_body_label(content, Texts.GAME_SUBTITLE)
        subtitle.pack(pady=(0, SPACING_MEDIUM))

        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.pack(pady=(0, SPACING_LARGE))
        self._add_choice_buttons(button_frame)

        toss_grid = ctk.CTkFrame(content, fg_color="transparent")
        toss_grid.pack(pady=(0, SPACING_MEDIUM))
        self._create_toss_labels(toss_grid)

        self._status_label = create_body_label(content, Texts.TOSS_PLACEHOLDER)
        self._status_label.pack()

    def _add_choice_buttons(self, master: ctk.CTkFrame) -> None:
        heads_button = self._create_choice_button(master, CoinSide.HEADS)
        tails_button = self._create_choice_button(master, CoinSide.TAILS)
        heads_button.pack(side="left", padx=(0, SPACING_SMALL))
        tails_button.pack(side="left", padx=(SPACING_SMALL, 0))
        self._choice_buttons.extend([heads_button, tails_button])

    def _create_choice_button(
        self,
        master: ctk.CTkFrame,
        side: CoinSide,
    ) -> ctk.CTkButton:
        return create_primary_button(
            master,
            side.value,
            lambda: self._start_game(side),
            width=CHOICE_BUTTON_WIDTH,
            height=CHOICE_BUTTON_HEIGHT,
        )

    def _create_toss_labels(self, master: ctk.CTkFrame) -> None:
        for index in range(COIN_TOSS_COUNT):
            label = ctk.CTkLabel(
                master,
                text=Texts.TOSS_UNKNOWN,
                width=TOSS_LABEL_WIDTH,
                height=TOSS_LABEL_HEIGHT,
                corner_radius=BUTTON_CORNER_RADIUS,
                fg_color=Colors.SURFACE,
                text_color=Colors.TEXT_DIM,
                font=ctk.CTkFont(size=14, weight="bold"),
            )
            label.grid(
                row=index // TOSS_COLUMNS,
                column=index % TOSS_COLUMNS,
                padx=SPACING_TINY,
                pady=SPACING_TINY,
            )
            self._toss_labels.append(label)

    def _start_game(self, selected_side: CoinSide) -> None:
        self._disable_choice_buttons()
        self._result = self.master.play_coin_toss(selected_side)
        self._revealed_tosses = 0
        self._update_status(Texts.SELECTED_SIDE_STATUS.format(side=selected_side.value))
        self._reveal_next_toss()

    def _disable_choice_buttons(self) -> None:
        for button in self._choice_buttons:
            button.configure(state="disabled")

    def _reveal_next_toss(self) -> None:
        if self._result is None:
            return

        if self._revealed_tosses >= self._result.total_rounds:
            self.after(TOSS_REVEAL_DELAY_MS, self._show_result)
            return

        toss = self._result.tosses[self._revealed_tosses]
        label = self._toss_labels[self._revealed_tosses]
        self._style_toss_label(label, toss)
        self._revealed_tosses += 1
        self.after(TOSS_REVEAL_DELAY_MS, self._reveal_next_toss)

    def _style_toss_label(self, label: ctk.CTkLabel, toss: CoinSide) -> None:
        label.configure(
            text=toss.value,
            fg_color=Colors.SURFACE_LIGHT,
            text_color=Colors.TEXT,
        )

    def _show_result(self) -> None:
        if self._result is not None:
            self._on_result(self._result)

    def _update_status(self, text: str) -> None:
        if self._status_label is not None:
            self._status_label.configure(text=text)


class ResultScreen(BaseScreen):
    def __init__(
        self,
        master: LuckMeterApp,
        result: GameResult,
        on_restart: Callable[[], None],
        on_home: Callable[[], None],
    ) -> None:
        super().__init__(master)
        self._result = result
        self._on_restart = on_restart
        self._on_home = on_home
        self._luck_score = calculate_luck_score(result.score)
        self._build()

    def _build(self) -> None:
        content = create_content_frame(self, padding_y=RESULT_SCREEN_PADDING_Y)

        title = create_title(content, Texts.RESULT_TITLE, size=RESULT_TITLE_FONT_SIZE)
        title.pack(pady=(0, SPACING_MEDIUM))

        self._create_score_line(
            content,
            Texts.POINTS_LABEL,
            Texts.PERCENT_VALUE.format(score=self._result.score),
        )
        self._create_score_line(
            content,
            Texts.LUCK_SCORE_LABEL,
            Texts.LUCK_SCORE_VALUE.format(score=self._luck_score),
        )

        detail = create_body_label(
            content,
            Texts.HITS_DETAIL.format(
                hits=self._result.hits,
                total_rounds=self._result.total_rounds,
            ),
        )
        detail.pack(pady=(SPACING_SMALL, SPACING_MEDIUM))

        message = ctk.CTkLabel(
            content,
            text=get_result_message(self._luck_score),
            font=ctk.CTkFont(size=RESULT_MESSAGE_FONT_SIZE, weight="bold"),
            text_color=Colors.TEXT,
            wraplength=CONTENT_WIDTH,
        )
        message.pack(pady=(0, SPACING_LARGE))

        restart_button = create_secondary_button(
            content,
            Texts.RESTART_BUTTON,
            self._on_restart,
        )
        restart_button.pack(pady=(0, SPACING_SMALL))

        home_button = create_primary_button(
            content,
            Texts.HOME_BUTTON,
            self._on_home,
        )
        home_button.pack()

    def _create_score_line(
        self,
        master: ctk.CTkFrame,
        label_text: str,
        value_text: str,
    ) -> None:
        label = create_body_label(master, label_text)
        label.pack()

        value = ctk.CTkLabel(
            master,
            text=value_text,
            font=ctk.CTkFont(size=SCORE_FONT_SIZE, weight="bold"),
            text_color=Colors.TEXT,
        )
        value.pack(pady=(0, SPACING_SMALL))


def create_content_frame(
    master: ctk.CTkFrame,
    padding_y: int = DEFAULT_SCREEN_PADDING_Y,
) -> ctk.CTkFrame:
    content = ctk.CTkFrame(master, fg_color="transparent", width=CONTENT_WIDTH)
    content.grid(row=0, column=0, padx=SCREEN_PADDING_X, pady=padding_y)
    return content


def create_title(
    master: ctk.CTkFrame,
    text: str,
    size: int,
) -> ctk.CTkLabel:
    return ctk.CTkLabel(
        master,
        text=text,
        font=ctk.CTkFont(size=size, weight="bold"),
        text_color=Colors.TEXT,
    )


def create_body_label(master: ctk.CTkFrame, text: str) -> ctk.CTkLabel:
    return ctk.CTkLabel(
        master,
        text=text,
        font=ctk.CTkFont(size=BODY_FONT_SIZE),
        text_color=Colors.TEXT_MUTED,
        wraplength=CONTENT_WIDTH,
    )


def create_primary_button(
    master: ctk.CTkFrame,
    text: str,
    command: Callable[[], None],
    width: int = PRIMARY_BUTTON_WIDTH,
    height: int = PRIMARY_BUTTON_HEIGHT,
) -> ctk.CTkButton:
    return create_button(
        master,
        text,
        command,
        width,
        height,
        Colors.PRIMARY,
        Colors.PRIMARY_HOVER,
    )


def create_secondary_button(
    master: ctk.CTkFrame,
    text: str,
    command: Callable[[], None],
) -> ctk.CTkButton:
    return create_button(
        master,
        text,
        command,
        PRIMARY_BUTTON_WIDTH,
        PRIMARY_BUTTON_HEIGHT,
        Colors.SURFACE_LIGHT,
        Colors.SURFACE_HOVER,
    )


def create_button(
    master: ctk.CTkFrame,
    text: str,
    command: Callable[[], None],
    width: int,
    height: int,
    fg_color: str,
    hover_color: str,
) -> ctk.CTkButton:
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        width=width,
        height=height,
        corner_radius=BUTTON_CORNER_RADIUS,
        fg_color=fg_color,
        hover_color=hover_color,
        text_color=Colors.WHITE,
        font=ctk.CTkFont(size=BUTTON_FONT_SIZE, weight="bold"),
    )
