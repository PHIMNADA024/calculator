import tkinter as tk


class Keypad(tk.Frame):

    def __init__(self, parent, keynames=None, columns=1, **kwargs) -> None:
        """Initialize Keypad object

        :param parent: Parent widget to which the Keypad belongs.
        :param keynames: List of strings representing the names or labels for the keys.
        :param columns: Number of columns to use for arranging the keys.
        """
        super().__init__(parent, **kwargs)
        if keynames is None:
            keynames = []
        self.buttons = []
        self.keynames = keynames
        self.init_components(columns)
        for index in range(self.grid_size()[1]):
            self.grid_rowconfigure(index, weight=1)
        for index in range(self.grid_size()[0]):
            self.grid_columnconfigure(index, weight=1)

    def init_components(self, columns: int) -> None:
        """Create a keypad of keys using the keynames list.
        The first keyname is at the top left of the keypad and
        fills the available columns left-to-right, adding as many
        rows as needed.

        :param columns: number of columns to use
        """
        current_row = 0
        current_column = 0
        for keyname, span in self.keynames:
            span = int(span)
            if current_column >= columns:
                current_column = 0
                current_row += 1
            button = tk.Button(self, text=keyname, width=3)
            button.grid(row=current_row, column=current_column, columnspan=span, sticky="nsew", pady=2, padx=2)
            self.buttons.append(button)
            current_column += span

    def bind(self, sequence=None, func=None, add=None) -> None:
        """Bind an event handler to an event sequence.

        :param sequence: Sequence of events to bind the handler to.
        :param func: Function to call when the event sequence occurs.
        :param add: Optional parameter indicating whether the binding should be
                    added to an existing binding or replaced.
        """
        for button in self.buttons:
            button.bind(sequence, func, add)

    def __setitem__(self, key: str, value: str) -> None:
        """Overrides __setitem__ to allow configuration of all buttons
        using dictionary syntax.

        Example: keypad['foreground'] = 'red'
        sets the font color on all buttons to red.

        :param key: Configuration key to set.
        :param value: Value to set for the given configuration key.
        """
        if key == 'font':
            for button in self.buttons:
                button.configure(font=value)
        else:
            super().__setitem__(key, value)

    def __getitem__(self, key: str):
        """Overrides __getitem__ to allow reading of configuration values
        from buttons.
        Example: keypad['foreground'] would return 'red' if the button
        foreground color is 'red'.

        param key: Configuration key to retrieve.
        :return: Value associated with the given configuration key.
        """
        if key == 'font':
            return self.buttons[0].__getitem__(key)
        else:
            return super().__getitem__(key)

    def configure(self, cnf=None, **kwargs) -> None:
        """Apply configuration settings to all buttons.

        To configure properties of the frame that contains the buttons,
        use `keypad.frame.configure()`.

        :param cnf: Configuration dictionary or keyword arguments to apply.
        :param kwargs: Additional keyword arguments to apply.
        """
        for button in self.buttons:
            button.configure(cnf, **kwargs)

    @property
    def frame(self) -> tk.Frame:
        """Returns the frame of the keypad.

        :return: The frame widget containing the keypad.
        """
        return super()
