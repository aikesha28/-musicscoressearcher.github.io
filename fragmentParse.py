import xml.etree.cElementTree as ET
import library


def setkeys(fifths, keys):
    reskeys = library.deffifths[fifths]
    if len(reskeys) >= 1:
        if reskeys[0] == 's':
            for i in range(1, len(reskeys)):
                keys[library.intnote[reskeys[i]]] = 1
        elif reskeys[0] == 'f':
            for i in range(1, len(reskeys)):
                keys[library.intnote[reskeys[i]]] = -1


def comp(arr1, arr2):
    for i in range(len(arr1)):
        if arr1[i] == arr2[i]:
            continue
        else:
            return 0
    return 1


def parseXML(MusicXML):
    tree = ET.ElementTree(file=MusicXML)
    root = tree.getroot()
    part = root.find('./part[1]')
    keys = [0] * 12
    takt = part.findall('measure')
    setkeys(part.find('./measure[1]/attributes/key/fifths').text,
            keys)  # тональность, может меняться в любой строчке поэтому нужно в каждом также проверять наличие

    return parse(takt, keys)


def parse(takt, keys):
    notes = []
    types = []
    note_to_calc = []
    types_to_calc = []
    i = 0
    while i < len(takt):
        if i == len(takt):
            break
        note = takt[i].findall("./note/[voice='1']")
        i = i + 1
        extract_info(note, notes, types, keys)

        note_to_calc = note_to_calc + notes
        types_to_calc = types_to_calc + types

        notes.clear()
        types.clear()
        note.clear()

    return calc_highs_and_weights(note_to_calc, types_to_calc)


def extract_info(note, notes, types, keys):
    count = 0
    length = len(note)
    while length > count + 1:
        if length > count + 1:
            while not note[count + 1].find('chord') == None:
                note.pop(count + 1)
                length = length - 1
                if length == count + 1:
                    break
        count = count + 1

    count = 0  # Удаляем все паузы в начале фрагмента, так как рассчитать внутренне представление должны от ноты
    if not note[0].find('rest') == None:  # нужно бы встроить проверку на длину массива
        if count + 1 < len(note):
            while not note[count + 1].find('rest') == None:
                note.pop(count)

    for k in range(len(note)):
        if note[k].find('rest') == None:
            alt = note[k].find('accidental')
            if not alt == None:
                altval = library.intalter[alt.text]
            else:
                altval = 3
            try:
                singlenote = library.intnote[note[k].find('./pitch/step').text]
                octave = int(note[k].find('./pitch/octave').text)
                # print(singlenote, octave, note[k].find('type').text)

                if altval == 0:
                    notes.append(singlenote + 12 * octave)  # необходимо проверить, а если си в первой октаве то это 11 + 12 * 0 = 11  а должно быть 11
                elif not altval == 3:
                    notes.append(
                        (singlenote + altval) + 12 * octave)  # необходимо проверить, а если си диез в первой октаве это до во второй 0+12*0=0 а должно быть 12
                else:
                    notes.append((singlenote + keys[singlenote]) + 12 * octave)
                types.append(note[k].find('type').text)  # тип ноты, то есть ее длительность
            except AttributeError:
                continue
        else:
            # print("- ", note[k].find('type').text)
            notes.append(None)
            types.append(note[k].find('type').text)


def calc_highs_and_weights(notes, types):
    highs = []
    weights = []
    inttypes = []
    prevNote = 0
    prevToCalcRest = 0

    for i in range(len(types)):
        inttypes.append(library.inttype[types[i]])

    for i in range(1, len(notes)):
        if notes[i] == None:
            highs.append(None)
            weights.append(inttypes[i] / inttypes[prevToCalcRest])
            prevToCalcRest = i
        else:
            highs.append(notes[i] - notes[prevNote])
            weights.append(inttypes[i] / inttypes[prevNote])
            prevNote = i
            prevToCalcRest = i

    initRepres = []
    for i in range(len(highs)):
        initRepres.append([highs[i], weights[i]])

    return initRepres


if __name__ == "__main__":
    # name = input("Введите названние файла:\n")
    x = parseXML("test1.xml")
    print("+fragment\n", x)
