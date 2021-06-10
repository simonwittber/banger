

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

