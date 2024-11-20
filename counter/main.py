import flet as ft
import math  # 팩토리얼 계산과 루트 사용


class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK


class CalculatorApp(ft.Container):
    # application's root control (i.e. "view") containing all other controls
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.width = 350
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            text="0", expand=2, button_clicked=self.button_clicked
                        ),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ActionButton(text="^", button_clicked=self.button_clicked),  # 제곱 버튼
                        ActionButton(text="/2", button_clicked=self.button_clicked),  # 나누기 2 버튼
                        ActionButton(text="√", button_clicked=self.button_clicked),  # 루트 버튼
                        ActionButton(text="!", button_clicked=self.button_clicked),  # 팩토리얼 버튼
                    ],
                    alignment="end",
                ),
                ft.Row(
                    controls=[
                        ActionButton(text="Prime?", button_clicked=self.button_clicked),  # 소수 판별 버튼
                    ],
                    alignment="end",
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand == True:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data

        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True

        elif data == "=":
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        elif data == "%":
            self.result.value = float(self.result.value) / 100
            self.reset()

        elif data == "+/-":
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)

            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )

        elif data == "^":  # 제곱 연산 처리
            try:
                self.result.value = self.format_number(float(self.result.value) ** 2)
            except Exception:
                self.result.value = "Error"

        elif data == "/2":  # 나누기 2 연산 처리
            try:
                self.result.value = self.format_number(float(self.result.value) / 2)
            except Exception:
                self.result.value = "Error"

        elif data == "√":  # 루트 연산 처리
            try:
                if float(self.result.value) < 0:
                    self.result.value = "Error"  # 음수의 루트는 계산 불가
                else:
                    self.result.value = self.format_number(math.sqrt(float(self.result.value)))
            except Exception:
                self.result.value = "Error"

        elif data == "!":  # 팩토리얼 연산 처리
            try:
                value = int(float(self.result.value))  # 소수점이 있는 정수를 처리
                if value < 0:
                    self.result.value = "Error"  # 음수는 팩토리얼 불가
                else:
                    self.result.value = math.factorial(value)
            except Exception:
                self.result.value = "Error"

        elif data == "Prime?":  # 소수 판별 처리
            try:
                value = int(float(self.result.value))  # 정수로 변환
                if value < 2:
                    self.result.value = "Not Prime"  # 2보다 작은 수는 소수가 아님
                else:
                    self.result.value = "Prime" if self.is_prime(value) else "Not Prime"
            except Exception:
                self.result.value = "Error"

        self.update()

    def is_prime(self, n):
        """소수 판별 함수"""
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(self, operand1, operand2, operator):

        if operator == "+":
            return self.format_number(operand1 + operand2)

        elif operator == "-":
            return self.format_number(operand1 - operand2)

        elif operator == "*":
            return self.format_number(operand1 * operand2)

        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Calc App with Prime Check"
    # create application instance
    calc = CalculatorApp()

    # add application's root control to the page
    page.add(calc)


ft.app(target=main)
