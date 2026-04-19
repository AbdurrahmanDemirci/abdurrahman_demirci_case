class Locator(tuple):
    """
    Selenium locator tuple with an auto-assigned name.

    Usage:
        class MyLocators:
            myPage_someElement_btn = Locator(By.CSS_SELECTOR, ".btn")

    Python calls __set_name__ automatically when the class body is processed,
    so myPage_someElement_btn.name == "myPage_someElement_btn" with no extra code.
    """

    def __new__(cls, by: str, value: str) -> "Locator":
        instance = super().__new__(cls, (by, value))
        instance.name = f"{by} '{value}'"  # fallback until __set_name__ fires
        return instance

    def __set_name__(self, _owner: type, name: str) -> None:
        self.name = name
