from math import *
import re
from snapshotManager import SnapshotManager


class Calculator:
    """Class for performing calculations."""

    def __init__(self):
        """Initialize the Calculator."""
        self.snapshot_manager = SnapshotManager()

    def calculate(self, equation: str, last_equation: list[str]) -> str:
        """Calculate the result of the equation.

        :param equation: The equation to calculate.
        :param last_equation: The list of the last equations.
        :return: The result of the calculation.
        """
        try:
            pattern = r"\(([^)]+)\)!"
            formatted_equation = re.sub(pattern, lambda match: f"factorial({match.group(1)})", equation)
            result = eval(formatted_equation.replace("^", "**"))
            self.save_snapshot(equation, result, last_equation)
            return result
        except Exception:
            return "Error"

    def save_snapshot(self, equation: str, result: str, last_equation: list[str]) -> None:
        """
        Save a snapshot of the equation and result.

        :param equation: The equation.
        :param result: The result of the equation.
        :param last_equation: The list of the last equations.

        """
        self.snapshot_manager.add_new_snapshot(equation, result, last_equation)

    def load_snapshot(self) -> list[tuple[str, list[str]]]:
        """Load all snapshots.

        :return: A list of snapshot equations and results.
        """
        return list(reversed(self.snapshot_manager.get_all_snapshot()))
