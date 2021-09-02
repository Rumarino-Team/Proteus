

# This function works both in python 2 and python 3.
def get_input(message=""):
    try:
        return raw_input(message)
    except NameError:
        return input(message)


def wait_for_enter():
    get_input("Press ENTER to continue: ")
