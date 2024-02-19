from snapshot import Snapshot


class SnapshotManager:
    """Class for managing snapshots of equations and results."""

    def __init__(self):
        """Initialize the SnapshotManager."""
        self.__snapshots = []

    @property
    def snapshots(self) -> list[Snapshot]:
        """Get the list of snapshots.

        :return:The list of snapshots.
        """
        return self.__snapshots

    def add_new_snapshot(self, equation: str, result: str, last_equation: list[str]) -> None:
        """Add a new snapshot to the list.

        :param equation: The equation for the snapshot.
        :param result: The result of the equation.
        :param last_equation: The list of the last equations.
        """
        new_snapshot = Snapshot(equation, result, last_equation)
        self.__snapshots.append(new_snapshot)

    def get_all_snapshot(self) -> list[tuple[str, list[str]]]:
        """Get all snapshots as a list of strings.

        :return: A list of strings representing the snapshots.
        """
        history_snapshots = []
        for snapshot in self.snapshots:
            last_equations = []
            for index in range(len(str(snapshot.result))):
                last_equations.append(str(snapshot.result)[:index])
            history_snapshots.append(("=" + str(snapshot.result), last_equations))
            history_snapshots.append((snapshot.equation, snapshot.last_equations))
        return history_snapshots
