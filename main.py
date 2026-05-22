from ui import LuckMeterApp


def main() -> None:
    app = LuckMeterApp()
    app.show_start_screen()
    app.mainloop()


if __name__ == "__main__":
    main()
