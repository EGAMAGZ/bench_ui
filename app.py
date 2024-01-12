import flet as ft
import subprocess
import re


def main(page: ft.Page, output: str) -> None:
    percentages, times = get_percentage_requests(output)
    test_info = get_test_info(output)
    data = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(percentage, time)
                for percentage, time in zip(percentages, times)
            ],
            stroke_width=5,
            color=ft.colors.CYAN,
            curved=True,
            stroke_cap_round=True,
        )
    ]

    chart = ft.LineChart(
        data_series=data,
        border=ft.border.all(3, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)),
        horizontal_grid_lines=ft.ChartGridLines(
            interval=1, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
        ),
        vertical_grid_lines=ft.ChartGridLines(
            interval=1, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
        ),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=min(times),
                    label=ft.Container(
                        ft.Text(
                            f"{(min(times)*100):.0f} ms",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
                ft.ChartAxisLabel(
                    value=max(times) / 2,
                    label=ft.Container(
                        ft.Text(
                            f"{((max(times)*100) / 2):.0f} ms",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
                ft.ChartAxisLabel(
                    value=max(times),
                    label=ft.Container(
                        ft.Text(
                            f"{(max(times)*100):.0f} ms",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
            ],
            labels_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=2.5,
                    label=ft.Text("25%", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=5.0,
                    label=ft.Text("50%", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=7.5,
                    label=ft.Text("75%", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=10,
                    label=ft.Text("100%", size=14, weight=ft.FontWeight.BOLD),
                ),
            ],
            labels_size=32,
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
        min_y=min(times),
        max_y=max(times),
        min_x=0,
        max_x=10,
        animate=2000,
        expand=True,
    )

    page.title = "Bench UI"
    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    value="Percentage of the requests served within a certain time (ms)",
                    style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                ),
                ft.Container(
                    content=chart,
                    padding=ft.padding.all(20),
                ),
            ],
        )
    )
    page.scroll = ft.ScrollMode.AUTO


def get_percentage_requests(output: str) -> tuple[list[int], list[int]]:
    pattern = r"(\d+)%\s+(\d+)"
    percentage_requests = re.findall(pattern, output)

    percentage_values = [int(match[0]) / 10 for match in percentage_requests]
    time_values = [int(match[1]) / 100 for match in percentage_requests]

    return percentage_values, time_values


def get_test_info(output: str) -> list[tuple[str, str]]:
    test_info = re.findall(
        r"([^:\n]+:[^\n]+)", re.search(r"Benchmarking(.+)", output, re.DOTALL).group(1)
    )

    return test_info


def get_integer_input(prompt):
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


if __name__ == "__main__":
    number_requests = get_integer_input("Enter the number of requests: ")
    number_multiple_requests = get_integer_input(
        "Enter the number of multiple requests: "
    )
    output = subprocess.check_output(
        f"abs -n {number_requests} -c {number_multiple_requests} https://minisaesipn.web.app/#/"
    ).decode()

    print(output)

    ft.app(target=lambda page: main(page=page, output=output))
