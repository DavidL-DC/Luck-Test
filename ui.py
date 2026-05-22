from collections.abc import Callable

import customtkinter as ctk


APP_TITLE = "Luck Meter"
WINDOW_SIZE = "420x420"
WINDOW_MIN_SIZE = 420
SPACING_SMALL = 8
SPACING_MEDIUM = 16
SPACING_LARGE = 28
CONTENT_WIDTH = 320


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
        self.configure(fg_color="#111318")

    def show_start_screen(self) -> None:
        self._set_screen(StartScreen(self, on_start=self.show_placeholder_screen))

    def show_placeholder_screen(self) -> None:
        self._set_screen(PlaceholderScreen(self, on_back=self.show_start_screen))

    def _set_screen(self, frame: ctk.CTkFrame) -> None:
        if self._active_frame is not None:
            self._active_frame.destroy()

        self._active_frame = frame
        self._active_frame.pack(fill="both", expand=True)


class BaseScreen(ctk.CTkFrame):
    def __init__(self, master: LuckMeterApp) -> None:
        super().__init__(master, fg_color="#111318", corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


class StartScreen(BaseScreen):
    def __init__(self, master: LuckMeterApp, on_start: Callable[[], None]) -> None:
        super().__init__(master)
        self._on_start = on_start
        self._build()

    def _build(self) -> None:
        content = ctk.CTkFrame(self, fg_color="transparent", width=CONTENT_WIDTH)
        content.grid(row=0, column=0, padx=40, pady=40)

        title = ctk.CTkLabel(
            content,
            text=APP_TITLE,
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#f4f7fb",
        )
        title.pack(pady=(0, SPACING_SMALL))

        subtitle = ctk.CTkLabel(
            content,
            text="Teste dein Glueck in kurzen Mini-Spielen.",
            font=ctk.CTkFont(size=14),
            text_color="#a8b0bd",
            wraplength=CONTENT_WIDTH,
        )
        subtitle.pack(pady=(0, SPACING_LARGE))

        start_button = ctk.CTkButton(
            content,
            text="Start",
            command=self._on_start,
            width=180,
            height=44,
            corner_radius=8,
            fg_color="#2f7df6",
            hover_color="#2567ca",
            text_color="#ffffff",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        start_button.pack()


class PlaceholderScreen(BaseScreen):
    def __init__(self, master: LuckMeterApp, on_back: Callable[[], None]) -> None:
        super().__init__(master)
        self._on_back = on_back
        self._build()

    def _build(self) -> None:
        content = ctk.CTkFrame(self, fg_color="transparent", width=CONTENT_WIDTH)
        content.grid(row=0, column=0, padx=40, pady=40)

        title = ctk.CTkLabel(
            content,
            text="Mini-Spiele folgen",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#f4f7fb",
        )
        title.pack(pady=(0, SPACING_MEDIUM))

        message = ctk.CTkLabel(
            content,
            text="Hier startet spaeter der interaktive Glueckstest.",
            font=ctk.CTkFont(size=14),
            text_color="#a8b0bd",
            wraplength=CONTENT_WIDTH,
        )
        message.pack(pady=(0, SPACING_LARGE))

        back_button = ctk.CTkButton(
            content,
            text="Zurueck",
            command=self._on_back,
            width=140,
            height=40,
            corner_radius=8,
            fg_color="#242933",
            hover_color="#303743",
            text_color="#ffffff",
        )
        back_button.pack()
