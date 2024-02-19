class Snapshot:
    """Class for representing a snapshot of an equation and its result."""

    def __init__(self, equation: str, result: str) -> None:
        """Initialize the Snapshot.

        :param equation: The equation for the snapshot.
        :param result: The result of the equation.
        """
        self.__equation = equation
        self.__result = result

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

    def __str__(self) -> str:
        """Return a string representation of the snapshot.

        :return: A string representing the equation and result.
        """
        return f"{self.__equation} = {self.__result}"
