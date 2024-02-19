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

    def add_new_snapshot(self, equation: str, result: str) -> None:
        """Add a new snapshot to the list.

        :param equation: The equation for the snapshot.
        :param result: The result of the equation.
        """
        new_snapshot = Snapshot(equation, result)
        self.__snapshots.append(new_snapshot)

    def get_all_snapshot(self) -> list[str]:
        """Get all snapshots as a list of strings.

        :return: A list of strings representing the snapshots.
        """
        history_snapshots = []
        for snapshot in self.snapshots:
            history_snapshots.append("=" + str(snapshot.result))
            history_snapshots.append(snapshot.equation)
        return history_snapshots
