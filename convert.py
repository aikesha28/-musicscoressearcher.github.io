import classes


def toNotes(x):
    notes = []  # строим фрагмент от ноты 0 длительностью 256(quarter)
    prevNote = classes.CommonNote(0, 256, x[0].isCommon, True)
    prevForType = classes.CommonNote(0, 256, x[0].isCommon, True)
    notes.append(prevNote)
    firsttime = False
    for i in range(len(x)):
        if not x[i].isNote:
            #print(i, " ", x[i].isCommon)
            c = classes.CommonNote(None, x[i].weight * prevForType.weight, x[i].isCommon, False)
            if x[i].isCommon and not firsttime:
                firsttime = True
                notes[i].isCommon = True
            prevForType = c
        else:
            #print(i, " ", x[i].isCommon)
            c = classes.CommonNote(x[i].high + prevNote.high, x[i].weight * prevNote.weight, x[i].isCommon, True)
            if x[i].isCommon and not firsttime:
                firsttime = True
                notes[i].isCommon = True
            prevNote = c
            prevForType = c
        notes.append(c)

    return notes


def toInt(x):
    intRepres = []  # строим фрагмент от ноты 0 длительностью 256(quarter)
    prevToRest = x[0]
    prevNote = x[0]
    for i in range(1, len(x)):
        if x[i].isNote:
            if x[i].isCommon:
                c = classes.CommonNote(x[i].high - prevNote.high, x[i].weight / prevNote.weight, True, True)
            else:
                c = classes.CommonNote(x[i].high - prevNote.high, x[i].weight / prevNote.weight, False, True)
            prevNote = x[i]
            prevToRest = x[i]
        else:
            if x[i].isCommon:
                c = classes.CommonNote(None, x[i].weight / prevNote.weight, True, False)
            else:
                c = classes.CommonNote(None, x[i].weight / prevNote.weight, False, False)
            prevToRest = x[i]
        intRepres.append(c)
    return intRepres
