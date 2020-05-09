import xml.etree.cElementTree as ET
import library
import psycopg2
import lcs
import classes

alpha = 0.5


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


def similiriaty(len_LCS, len_x, len_y, N):
    return 2 * len_LCS / (len_x + len_y + alpha * N)


def parseXML(MusicXML):
    tree = ET.ElementTree(file=MusicXML)
    root = tree.getroot()
    result = []

    part = root.findall('part')

    for i in range(len(part)):
        keys = [0] * 12
        stave = part[i].find('./measure[1]/attributes/staves')
        setkeys(part[i].find('./measure[1]/attributes/key/fifths').text, keys)
        takt = part[i].findall('measure')
        if not stave == None:
            more_staff(takt, int(stave.text), keys, result)
        else:
            one_staff(takt, keys, result)

    return result


def one_staff(takt, keys, result):
    notes = []
    types = []
    note = []
    takts = [2, 4, 8]
    for l in takts:
        i = 0
        while i < len(takt):
            for j in range(l):
                if i == len(takt):
                    break
                note = note + takt[i].findall("./note/[voice='1']")
                i = i + 1
            extract_info(note, notes, types, keys)

            int_repres = calc_highs_and_weights(notes, types)
            if len(int_repres) > 5:
                result.append(int_repres)

            notes.clear()
            types.clear()
            note.clear()


def more_staff(takt, staves, keys, result):
    for i in range(staves):
        notes = []
        types = []
        note_by_hand = []
        takts = [2, 4, 8]

        for l in takts:
            j = 0
            while j < len(takt):
                for k in range(l):
                    if j == len(takt):
                        break
                    note_by_hand = note_by_hand + takt[j].findall("./note/[staff='%d']" % (i + 1))
                    j = j + 1
                voice = note_by_hand[0].find("voice").text
                note = []
                for k in range(len(note_by_hand)):
                    loc_voice = note_by_hand[k].find("voice")
                    if loc_voice.text == voice:
                        note.append(note_by_hand[k])  # ноты соответсвующие i-ой руке и голосу с первой "ноты"

                extract_info(note, notes, types, keys)

                int_repres = calc_highs_and_weights(notes, types)
                if len(int_repres) > 5:
                    result.append(int_repres)

                notes.clear()
                types.clear()
                note_by_hand.clear()


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
    if not note[count].find('rest') == None:
        while True:
            if count + 1 < len(note):
                break
            if not note[count + 1].find('rest') == None:
                note.pop(count)
            else:
                break
    print("-----------------GameOfThronesEasy.xml")
    print(note)
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
            if note[k].find('type') != None:
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
    name = input("Введите названние файла:\n")
    title = input("Введите название произведения:\n")
    author = input("Введите автора:\n")
    url = input("Введите url:\n")

    conn = psycopg2.connect(dbname='dcl2ubhc941p22', user='xzeuappslxemeh', password='4d83afb05b3f71fd67f84854159dfe1600a859945176f13cf92f8eb098d96e40',
                            host='ec2-46-137-91-216.eu-west-1.compute.amazonaws.com', port='5432')
    cursor = conn.cursor()

    # Выполняем запрос.
    cursor.execute("SELECT * FROM notations WHERE title = \'" + title + "\' AND author  = \'" + author + "\'")
    row = cursor.fetchone()
    if row == None:
        cursor.execute("SELECT max(code) FROM notations")
        codes = cursor.fetchone()
        notation_code = codes[0] + 1
        cursor.execute("SELECT max(code) FROM internal_representation")
        codes = cursor.fetchone()
        int_repres_code = codes[0]
        cursor.execute("INSERT INTO notations VALUES (" + str(notation_code) + ",\'" + title + "\',\'" + author + "\',\'" + url + "\');")

        result = parseXML(name)
        cursor.execute("SELECT * FROM internal_representation")
        while True:
            int_repres_row = cursor.fetchone()
            if int_repres_row == None:
                break

            int_repres = int_repres_row[1]

            int_y = []  # Записываем фрагмент из базы как массив элеметнов класса CommonNote
            for i in range(len(int_repres)):
                c = classes.CommonNote(int_repres[i][0], float(int_repres[i][1]), False, not int_repres[i][0] == None)
                int_y.append(c)

            for i in range(len(result)):
                int_x = []  # Записываем фрагмент из результирующего списка как массив элеметнов класса CommonNote
                for j in range(len(result[i])):
                    c = classes.CommonNote(result[i][j][0], result[i][j][1], False, not result[i][j][0] == None)
                    int_x.append(c)
                    if similiriaty(len(lcs.LCS_DYN(int_x, int_y)), len(int_x), len(int_y), 0) >= 0.98:
                        del result[i]
                del int_x
        for i in range(len(result)):
            print("-----------------GameOfThronesEasy.xml")
            print(result[i])
            int_repres_code += 1
            res = "{"
            for j in range(len(result[i])):
                if j == 0:
                    res = res + "{" + str(result[i][j][0]) + ","
                    res = res + str(result[i][j][1]) + "}"
                else:
                    res = res + ",{" + str(result[i][j][0]) + ","
                    res = res + str(result[i][j][1]) + "}"
            res = res + "}"
            print(res)
            print("INSERT INTO internal_representation VALUES (" + str(int_repres_code) + ",\'" + res + "\'," + str(notation_code) + "); COMMIT;")
            cursor.execute("INSERT INTO internal_representation VALUES (" + str(int_repres_code) + ",\'" + res + "\'," + str(notation_code) + "); COMMIT;")
