
def confirm(message, default=None):
    if default is None:
        suffix = "(y/n)"
    else:
        suffix = "([y]/n)" if default else "(y/[n])"
    while True:
        choice = input("%s %s? "%(message, suffix)).lower()
        if choice == "" and default is not None:
            return default
        if choice == "y":
            return True
        if choice == "n":
            return False


def choice(message, items):
    things = list(items)
    for i,p in enumerate(things):
        line = "[%s]"%i
        spacing = " " * (6-len(line))
        print("%s%s%s"%(line, spacing,p))
    choice = input("Choose 0 - %s: "%len(things))
    try:
        index  = int(choice)
    except:
        return None
    return things[index]

