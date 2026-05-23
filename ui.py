from collections.abc import Callable

import customtkinter as ctk

from games import (
    COIN_TOSS_COUNT,
    LUCKY_NUMBER_MAX,
    LUCKY_NUMBER_MIN,
    TREASURE_GRID_SIZE,
    TREASURE_OPEN_COUNT,
    CoinSide,
    CoinTossGame,
    CoinTossResult,
    LuckyNumberGame,
    LuckyNumberResult,
    RiskWheelGame,
    RiskWheelResult,
    TreasureChest,
    TreasureChestGame,
    TreasureChestResult,
)
from scoring import (
    calculate_average_score,
    calculate_luck_score,
    get_result_message,
)


APP_TITLE = "Luck Meter"
WINDOW_SIZE = "420x420"
WINDOW_MIN_SIZE = 420
SCREEN_PADDING_X = 40
DEFAULT_SCREEN_PADDING_Y = 38
RESULT_SCREEN_PADDING_Y = 30
SPACING_TINY = 4
SPACING_SMALL = 8
SPACING_MEDIUM = 14
SPACING_LARGE = 24
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
RESULT_TITLE_FONT_SIZE = 26
BODY_FONT_SIZE = 14
BUTTON_FONT_SIZE = 14
RESULT_MESSAGE_FONT_SIZE = 14
SCORE_FONT_SIZE = 26
SMALL_SCORE_FONT_SIZE = 20
TREASURE_BUTTON_WIDTH = 86
TREASURE_BUTTON_HEIGHT = 44
WHEEL_SPIN_STEPS = 8
WHEEL_SPIN_DELAY_MS = 90


class Texts:
    APP_TITLE = "Luck Meter"
    START_SUBTITLE = "Teste dein Glück in kurzen Mini-Spielen."
    START_BUTTON = "Start"
    COIN_TITLE = "Münzwurf-Serie"
    COIN_SUBTITLE = "Wähle eine Seite. Danach fallen 10 Münzen."
    LUCKY_TITLE = "Glückszahl"
    LUCKY_SUBTITLE = (
        f"Wähle eine Zahl von {LUCKY_NUMBER_MIN} bis {LUCKY_NUMBER_MAX}."
    )
    TREASURE_TITLE = "Schatzkisten"
    TREASURE_SUBTITLE = f"Öffne genau {TREASURE_OPEN_COUNT} Kisten."
    CHEST_CLOSED = "Kiste"
    TREASURE_STATUS = "{opened} von {required} Kisten geöffnet"
    RISK_TITLE = "Risiko-Rad"
    RISK_SUBTITLE = "Drehe das Rad und nimm, was kommt."
    SPIN_BUTTON = "Rad drehen"
    SPINNING_TEXTS = ("Mega-Glück", "Glück", "Neutral", "Pech")
    RISK_RESULT = "{outcome}"
    DRAW_BUTTON = "Zahl ziehen"
    NEXT_GAME_BUTTON = "Weiter"
    SHOW_RESULT_BUTTON = "Ergebnis anzeigen"
    SELECTED_NUMBER = "Gewählt: {number}"
    DRAWN_NUMBER = "Gezogen: {number}"
    DIFFERENCE = "Differenz: {difference}"
    GAME_POINTS = "Punkte: {score:.1f}%"
    TOSS_PLACEHOLDER = "Bereit"
    TOSS_UNKNOWN = "?"
    RESULT_TITLE = "Ergebnis"
    COIN_SCORE_LABEL = "Münzwurf-Serie"
    LUCKY_SCORE_LABEL = "Glückszahl"
    TREASURE_SCORE_LABEL = "Schatzkisten"
    RISK_SCORE_LABEL = "Risiko-Rad"
    AVERAGE_LABEL = "Durchschnitt"
    LUCK_SCORE_LABEL = "Luck Score"
    SELECTED_SIDE_STATUS = "Gewählt: {side}"
    HITS_DETAIL = "{hits} von {total_rounds} Treffern"
    COIN_DONE_STATUS = "{hits} von {total_rounds} Treffern"
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
        self._lucky_number_game = LuckyNumberGame()
        self._treasure_chest_game = TreasureChestGame()
        self._risk_wheel_game = RiskWheelGame()
        self._coin_result: CoinTossResult | None = None
        self._lucky_result: LuckyNumberResult | None = None
        self._treasure_result: TreasureChestResult | None = None
        self._risk_result: RiskWheelResult | None = None
        self.configure(fg_color=Colors.BACKGROUND)

    def show_start_screen(self) -> None:
        self._coin_result = None
        self._lucky_result = None
        self._treasure_result = None
        self._risk_result = None
        self._set_screen(StartScreen(self, on_start=self.show_coin_toss_screen))

    def show_coin_toss_screen(self) -> None:
        self._coin_result = None
        self._lucky_result = None
        self._treasure_result = None
        self._risk_result = None
        screen = CoinTossScreen(
            self,
            on_complete=self.show_lucky_number_screen,
        )
        self._set_screen(screen)

    def show_lucky_number_screen(self, coin_result: CoinTossResult) -> None:
        self._coin_result = coin_result
        screen = LuckyNumberScreen(
            self,
            options=self._lucky_number_game.get_options(),
            on_complete=self.show_treasure_chest_screen,
        )
        self._set_screen(screen)

    def show_treasure_chest_screen(self, lucky_result: LuckyNumberResult) -> None:
        if self._coin_result is None:
            self.show_start_screen()
            return

        self._lucky_result = lucky_result
        screen = TreasureChestScreen(
            self,
            chests=self._treasure_chest_game.create_chests(),
            on_complete=self.show_risk_wheel_screen,
        )
        self._set_screen(screen)

    def show_risk_wheel_screen(self, treasure_result: TreasureChestResult) -> None:
        if self._coin_result is None or self._lucky_result is None:
            self.show_start_screen()
            return

        self._treasure_result = treasure_result
        screen = RiskWheelScreen(
            self,
            on_complete=self.show_result_screen,
        )
        self._set_screen(screen)

    def show_result_screen(self, risk_result: RiskWheelResult) -> None:
        missing_result = (
            self._coin_result is None
            or self._lucky_result is None
            or self._treasure_result is None
        )
        if missing_result:
            self.show_start_screen()
            return

        self._risk_result = risk_result
        screen = ResultScreen(
            self,
            coin_result=self._coin_result,
            lucky_result=self._lucky_result,
            treasure_result=self._treasure_result,
            risk_result=risk_result,
            on_restart=self.show_coin_toss_screen,
            on_home=self.show_start_screen,
        )
        self._set_screen(screen)

    def play_coin_toss(self, selected_side: CoinSide) -> CoinTossResult:
        return self._coin_game.play(selected_side)

    def play_lucky_number(self, selected_number: int) -> LuckyNumberResult:
        return self._lucky_number_game.play(selected_number)

    def score_treasure_chests(
        self,
        opened_chests: list[TreasureChest],
    ) -> TreasureChestResult:
        return self._treasure_chest_game.score_opened_chests(opened_chests)

    def spin_risk_wheel(self) -> RiskWheelResult:
        return self._risk_wheel_game.spin()

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
        on_complete: Callable[[CoinTossResult], None],
    ) -> None:
        super().__init__(master)
        self._on_complete = on_complete
        self._result: CoinTossResult | None = None
        self._revealed_tosses = 0
        self._choice_buttons: list[ctk.CTkButton] = []
        self._toss_labels: list[ctk.CTkLabel] = []
        self._status_label: ctk.CTkLabel | None = None
        self._next_button: ctk.CTkButton | None = None
        self._build()

    def _build(self) -> None:
        content = create_content_frame(self)

        title = create_title(content, Texts.COIN_TITLE, size=GAME_TITLE_FONT_SIZE)
        title.pack(pady=(0, SPACING_SMALL))

        subtitle = create_body_label(content, Texts.COIN_SUBTITLE)
        subtitle.pack(pady=(0, SPACING_MEDIUM))

        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.pack(pady=(0, SPACING_LARGE))
        self._add_choice_buttons(button_frame)

        toss_grid = ctk.CTkFrame(content, fg_color="transparent")
        toss_grid.pack(pady=(0, SPACING_MEDIUM))
        self._create_toss_labels(toss_grid)

        self._status_label = create_body_label(content, Texts.TOSS_PLACEHOLDER)
        self._status_label.pack()

        self._next_button = create_primary_button(
            content,
            Texts.NEXT_GAME_BUTTON,
            self._show_next_game,
        )

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
                font=ctk.CTkFont(size=BODY_FONT_SIZE, weight="bold"),
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
            self._show_continue_button()
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

    def _show_next_game(self) -> None:
        if self._result is not None:
            self._on_complete(self._result)

    def _show_continue_button(self) -> None:
        if self._result is None or self._next_button is None:
            return

        self._update_status(
            Texts.COIN_DONE_STATUS.format(
                hits=self._result.hits,
                total_rounds=self._result.total_rounds,
            )
        )
        self._next_button.pack(pady=(SPACING_MEDIUM, 0))

    def _update_status(self, text: str) -> None:
        if self._status_label is not None:
            self._status_label.configure(text=text)


class LuckyNumberScreen(BaseScreen):
    def __init__(
        self,
        master: LuckMeterApp,
        options: list[int],
        on_complete: Callable[[LuckyNumberResult], None],
    ) -> None:
        super().__init__(master)
        self._on_complete = on_complete
        self._selected_value = ctk.StringVar(value=str(options[0]))
        self._number_options = [str(option) for option in options]
        self._result_labels: list[ctk.CTkLabel] = []
        self._selector: ctk.CTkOptionMenu | None = None
        self._draw_button: ctk.CTkButton | None = None
        self._next_button: ctk.CTkButton | None = None
        self._result: LuckyNumberResult | None = None
        self._build()

    def _build(self) -> None:
        content = create_content_frame(self)

        title = create_title(content, Texts.LUCKY_TITLE, size=GAME_TITLE_FONT_SIZE)
        title.pack(pady=(0, SPACING_SMALL))

        subtitle = create_body_label(content, Texts.LUCKY_SUBTITLE)
        subtitle.pack(pady=(0, SPACING_LARGE))

        self._selector = ctk.CTkOptionMenu(
            content,
            values=self._number_options,
            variable=self._selected_value,
            width=PRIMARY_BUTTON_WIDTH,
            height=PRIMARY_BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=Colors.SURFACE_LIGHT,
            button_color=Colors.PRIMARY,
            button_hover_color=Colors.PRIMARY_HOVER,
            text_color=Colors.WHITE,
        )
        self._selector.pack(pady=(0, SPACING_MEDIUM))

        self._draw_button = create_primary_button(
            content,
            Texts.DRAW_BUTTON,
            self._play_game,
        )
        self._draw_button.pack(pady=(0, SPACING_LARGE))

        result_frame = ctk.CTkFrame(content, fg_color="transparent")
        result_frame.pack()
        self._create_result_labels(result_frame)

        self._next_button = create_primary_button(
            content,
            Texts.NEXT_GAME_BUTTON,
            self._show_result_screen,
        )

    def _create_result_labels(self, master: ctk.CTkFrame) -> None:
        for _ in range(4):
            label = create_body_label(master, "")
            label.pack(pady=(0, SPACING_SMALL))
            self._result_labels.append(label)

    def _play_game(self) -> None:
        if self._draw_button is not None:
            self._draw_button.configure(state="disabled")

        selected_number = int(self._selected_value.get())
        self._result = self.master.play_lucky_number(selected_number)
        self._hide_input_controls()
        self._show_result(self._result)
        self._show_continue_button()

    def _hide_input_controls(self) -> None:
        if self._selector is not None:
            self._selector.pack_forget()

        if self._draw_button is not None:
            self._draw_button.pack_forget()

    def _show_result(self, result: LuckyNumberResult) -> None:
        texts = [
            Texts.SELECTED_NUMBER.format(number=result.selected_number),
            Texts.DRAWN_NUMBER.format(number=result.drawn_number),
            Texts.DIFFERENCE.format(difference=result.difference),
            Texts.GAME_POINTS.format(score=result.score),
        ]

        for label, text in zip(self._result_labels, texts, strict=True):
            label.configure(text=text)

    def _show_continue_button(self) -> None:
        if self._next_button is not None:
            self._next_button.pack(pady=(SPACING_MEDIUM, 0))

    def _show_result_screen(self) -> None:
        if self._result is not None:
            self._on_complete(self._result)


class TreasureChestScreen(BaseScreen):
    def __init__(
        self,
        master: LuckMeterApp,
        chests: list[TreasureChest],
        on_complete: Callable[[TreasureChestResult], None],
    ) -> None:
        super().__init__(master)
        self._chests = chests
        self._on_complete = on_complete
        self._opened_indices: list[int] = []
        self._chest_buttons: list[ctk.CTkButton] = []
        self._status_label: ctk.CTkLabel | None = None
        self._next_button: ctk.CTkButton | None = None
        self._result: TreasureChestResult | None = None
        self._build()

    def _build(self) -> None:
        content = create_content_frame(self, padding_y=RESULT_SCREEN_PADDING_Y)

        title = create_title(content, Texts.TREASURE_TITLE, size=GAME_TITLE_FONT_SIZE)
        title.pack(pady=(0, SPACING_SMALL))

        subtitle = create_body_label(content, Texts.TREASURE_SUBTITLE)
        subtitle.pack(pady=(0, SPACING_MEDIUM))

        grid = ctk.CTkFrame(content, fg_color="transparent")
        grid.pack(pady=(0, SPACING_MEDIUM))
        self._create_chest_buttons(grid)

        self._status_label = create_body_label(content, self._get_status_text())
        self._status_label.pack()

        self._next_button = create_primary_button(
            content,
            Texts.SHOW_RESULT_BUTTON,
            self._show_result_screen,
        )

    def _create_chest_buttons(self, master: ctk.CTkFrame) -> None:
        for index, _chest in enumerate(self._chests):
            button = create_secondary_button(
                master,
                Texts.CHEST_CLOSED,
                lambda chest_index=index: self._open_chest(chest_index),
                width=TREASURE_BUTTON_WIDTH,
                height=TREASURE_BUTTON_HEIGHT,
            )
            button.grid(
                row=index // TREASURE_GRID_SIZE,
                column=index % TREASURE_GRID_SIZE,
                padx=SPACING_TINY,
                pady=SPACING_TINY,
            )
            self._chest_buttons.append(button)

    def _open_chest(self, index: int) -> None:
        if self._result is not None or index in self._opened_indices:
            return

        self._opened_indices.append(index)
        chest = self._chests[index]
        button = self._chest_buttons[index]
        button.configure(
            text=f"{chest.label}\n{chest.points}",
            state="disabled",
            fg_color=Colors.SURFACE_LIGHT,
        )
        self._update_status()

        if len(self._opened_indices) == TREASURE_OPEN_COUNT:
            self._finish_game()

    def _finish_game(self) -> None:
        opened_chests = [self._chests[index] for index in self._opened_indices]
        self._result = self.master.score_treasure_chests(opened_chests)
        self._disable_closed_chests()
        self._show_continue_button()

    def _disable_closed_chests(self) -> None:
        for index, button in enumerate(self._chest_buttons):
            if index not in self._opened_indices:
                button.configure(state="disabled")

    def _show_continue_button(self) -> None:
        if self._next_button is not None:
            self._next_button.pack(pady=(SPACING_MEDIUM, 0))

    def _show_result_screen(self) -> None:
        if self._result is not None:
            self._on_complete(self._result)

    def _update_status(self) -> None:
        if self._status_label is not None:
            self._status_label.configure(text=self._get_status_text())

    def _get_status_text(self) -> str:
        return Texts.TREASURE_STATUS.format(
            opened=len(self._opened_indices),
            required=TREASURE_OPEN_COUNT,
        )


class RiskWheelScreen(BaseScreen):
    def __init__(
        self,
        master: LuckMeterApp,
        on_complete: Callable[[RiskWheelResult], None],
    ) -> None:
        super().__init__(master)
        self._on_complete = on_complete
        self._result: RiskWheelResult | None = None
        self._spin_button: ctk.CTkButton | None = None
        self._next_button: ctk.CTkButton | None = None
        self._outcome_label: ctk.CTkLabel | None = None
        self._points_label: ctk.CTkLabel | None = None
        self._spin_step = 0
        self._build()

    def _build(self) -> None:
        content = create_content_frame(self)

        title = create_title(content, Texts.RISK_TITLE, size=GAME_TITLE_FONT_SIZE)
        title.pack(pady=(0, SPACING_SMALL))

        subtitle = create_body_label(content, Texts.RISK_SUBTITLE)
        subtitle.pack(pady=(0, SPACING_LARGE))

        self._outcome_label = ctk.CTkLabel(
            content,
            text="?",
            width=220,
            height=72,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=Colors.SURFACE,
            text_color=Colors.TEXT,
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self._outcome_label.pack(pady=(0, SPACING_MEDIUM))

        self._points_label = create_body_label(content, "")
        self._points_label.pack(pady=(0, SPACING_LARGE))

        self._spin_button = create_primary_button(
            content,
            Texts.SPIN_BUTTON,
            self._start_spin,
        )
        self._spin_button.pack()

        self._next_button = create_primary_button(
            content,
            Texts.SHOW_RESULT_BUTTON,
            self._show_result_screen,
        )

    def _start_spin(self) -> None:
        if self._spin_button is not None:
            self._spin_button.configure(state="disabled")

        self._result = self.master.spin_risk_wheel()
        self._spin_step = 0
        self._animate_spin()

    def _animate_spin(self) -> None:
        if self._spin_step >= WHEEL_SPIN_STEPS:
            self._show_spin_result()
            return

        text_index = self._spin_step % len(Texts.SPINNING_TEXTS)
        self._set_outcome_text(Texts.SPINNING_TEXTS[text_index])
        self._spin_step += 1
        self.after(WHEEL_SPIN_DELAY_MS, self._animate_spin)

    def _show_spin_result(self) -> None:
        if self._result is None:
            return

        self._set_outcome_text(
            Texts.RISK_RESULT.format(outcome=self._result.outcome.label)
        )
        if self._points_label is not None:
            self._points_label.configure(
                text=Texts.GAME_POINTS.format(score=self._result.score)
            )

        if self._next_button is not None:
            self._next_button.pack(pady=(SPACING_MEDIUM, 0))

    def _set_outcome_text(self, text: str) -> None:
        if self._outcome_label is not None:
            self._outcome_label.configure(text=text)

    def _show_result_screen(self) -> None:
        if self._result is not None:
            self._on_complete(self._result)


class ResultScreen(BaseScreen):
    def __init__(
        self,
        master: LuckMeterApp,
        coin_result: CoinTossResult,
        lucky_result: LuckyNumberResult,
        treasure_result: TreasureChestResult,
        risk_result: RiskWheelResult,
        on_restart: Callable[[], None],
        on_home: Callable[[], None],
    ) -> None:
        super().__init__(master)
        self._coin_result = coin_result
        self._lucky_result = lucky_result
        self._treasure_result = treasure_result
        self._risk_result = risk_result
        self._on_restart = on_restart
        self._on_home = on_home
        self._average_score = calculate_average_score(self._get_game_scores())
        self._luck_score = calculate_luck_score(self._average_score)
        self._build()

    def _build(self) -> None:
        content = create_content_frame(self, padding_y=RESULT_SCREEN_PADDING_Y)

        title = create_title(content, Texts.RESULT_TITLE, size=RESULT_TITLE_FONT_SIZE)
        title.pack(pady=(0, SPACING_MEDIUM))

        self._create_score_line(
            content,
            Texts.COIN_SCORE_LABEL,
            Texts.PERCENT_VALUE.format(score=self._coin_result.score),
        )
        self._create_score_line(
            content,
            Texts.LUCKY_SCORE_LABEL,
            Texts.PERCENT_VALUE.format(score=self._lucky_result.score),
        )
        self._create_score_line(
            content,
            Texts.TREASURE_SCORE_LABEL,
            Texts.PERCENT_VALUE.format(score=self._treasure_result.score),
        )
        self._create_score_line(
            content,
            Texts.RISK_SCORE_LABEL,
            Texts.PERCENT_VALUE.format(score=self._risk_result.score),
        )
        self._create_score_line(
            content,
            Texts.AVERAGE_LABEL,
            Texts.PERCENT_VALUE.format(score=self._average_score),
        )
        self._create_score_line(
            content,
            Texts.LUCK_SCORE_LABEL,
            Texts.LUCK_SCORE_VALUE.format(score=self._luck_score),
            large=True,
        )

        message = ctk.CTkLabel(
            content,
            text=get_result_message(self._luck_score),
            font=ctk.CTkFont(size=RESULT_MESSAGE_FONT_SIZE, weight="bold"),
            text_color=Colors.TEXT,
            wraplength=CONTENT_WIDTH,
        )
        message.pack(pady=(SPACING_SMALL, SPACING_MEDIUM))

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

    def _get_game_scores(self) -> list[float]:
        return [
            self._coin_result.score,
            self._lucky_result.score,
            self._treasure_result.score,
            self._risk_result.score,
        ]

    def _create_score_line(
        self,
        master: ctk.CTkFrame,
        label_text: str,
        value_text: str,
        large: bool = False,
    ) -> None:
        row = ctk.CTkFrame(master, fg_color="transparent")
        row.pack(fill="x", pady=(0, SPACING_SMALL))

        label = create_body_label(row, label_text)
        label.pack(side="left")

        font_size = SCORE_FONT_SIZE if large else SMALL_SCORE_FONT_SIZE
        value = ctk.CTkLabel(
            row,
            text=value_text,
            font=ctk.CTkFont(size=font_size, weight="bold"),
            text_color=Colors.TEXT,
        )
        value.pack(side="right")


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
    width: int = PRIMARY_BUTTON_WIDTH,
    height: int = PRIMARY_BUTTON_HEIGHT,
) -> ctk.CTkButton:
    return create_button(
        master,
        text,
        command,
        width,
        height,
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
