class Snapshot:
    """Class for representing a snapshot of an equation and its result."""

    def __init__(self, equation: str, result: str, last_equations: list[str]) -> None:
        """Initialize the Snapshot.

        :param equation: The equation for the snapshot.
        :param result: The result of the equation.
        """
        self.__equation = equation
        self.__result = result
        self.__last_equations = last_equations

    @property
    def equation(self) -> str:
        """Get the equation of the snapshot.

        :return: The equation.
        """
        return self.__equation

    @property
    def result(self) -> str:
        """Get the result of the snapshot.

        :return: The result.
        """
        return self.__result

    @property
    def last_equations(self) -> list[str]:
        """Get list of the last equation.

        :return: List of last equation.
        """
        return self.__last_equations

    def __str__(self) -> str:
        """Return a string representation of the snapshot.

        :return: A string representing the equation and result.
        """
        return f"{self.__equation} = {self.__result}"
