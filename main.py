from menu import *


if __name__ == '__main__':
    win = Contacts()
    win.show()
    win.setMinimumSize(450, 600)
    win.setMaximumSize(450, 600)

    sys.exit(app.exec())
