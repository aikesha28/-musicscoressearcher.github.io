import psycopg2
import fragmentParse
import lcs
import rules
import convert
import classes

alpha = 0.5


def compare(int_x, int_y):
    N = 0
    LCS = lcs.LCS_DYN(int_x, int_y)
    #x = convert.toNotes(int_x)
    #y = convert.toNotes(int_y)
    #len_LCS = 0
    #for i in range(len(x)):
    #    if x[i].isCommon:
    #        len_LCS += 1

    if (len(LCS) > min(len(int_x), len(int_y)) / 2):
        rules.deleteTails(int_x, int_y)
        print("2)", len(LCS), len(int_x), len(int_y))
        print("2)", similiriaty(len(LCS), len(int_x), len(int_y), N))
        print("2)", len(LCS), len(int_x), len(int_y))
        if similiriaty(len(LCS), len(int_x), len(int_y), N) > 0.90:
            return True
        else:
            N += rules.firstRule(int_x)
            N += rules.firstRule(int_y)
            N += rules.secondRule(int_x)
            N += rules.secondRule(int_y)
            N += rules.thirdRule(int_x)
            N += rules.thirdRule(int_y)

            N += rules.correctMistakes(int_x, int_y)
            # N += rules.final(x, y)
            if N > 0:
                LCS = lcs.LCS_DYN(int_x, int_y)
                #len_LCS = 0
                #for i in range(len(int_x)):
                #    if x[i].isCommon:
                #        len_LCS += 1
            print("N = ", N)
            print("3)", similiriaty(len(LCS), len(int_x), len(int_y), N))
            print("3)", len(LCS), len(int_x), len(int_y))
            if similiriaty(len(LCS), len(int_x), len(int_y), N) > 0.90:
                return True
            else:
                return False
    else:
        return 0


def similiriaty(len_LCS, len_x, len_y, N):
    return 2 * len_LCS / (len_x + len_y + alpha * N)


def search(x):
    res = []
    results = []
    conn = psycopg2.connect(dbname='dcl2ubhc941p22', user='xzeuappslxemeh', password='4d83afb05b3f71fd67f84854159dfe1600a859945176f13cf92f8eb098d96e40',
                            host='ec2-46-137-91-216.eu-west-1.compute.amazonaws.com', port='5432')
    cursor = conn.cursor()

    # Выполняем запрос.
    cursor.execute("SELECT * FROM internal_representation")

    # Цикл по фрагментам из базы
    while True:
        row = cursor.fetchone()
        if row == None:
            break  # Если больше в таблице нет фрагментов то выходим

        int_repres = row[1]  # внутреннее представление хранится во второй колонке таблицы

        print("НОВЫЙ ЭЛЕМЕНТ - ", row[0])
        int_x= []  # Записываем входящий фрагмент как массив элеметнов класса CommonNote
        for i in range(len(x)):
            c = classes.CommonNote(x[i][0], x[i][1], False, not x[i][0] == None)
            int_x.append(c)

        int_y = []  # Записываем фрагмент из базы как массив элеметнов класса CommonNote
        for i in range(len(int_repres)):
            c = classes.CommonNote(int_repres[i][0], float(int_repres[i][1]), False, not int_repres[i][0] == None)
            int_y.append(c)

        if compare(int_x, int_y):  # Сравниваем
            res.append(row[2])

        del int_x
        del int_y

    # Закрываем подключение.
    id_of_res=[]
    for i in range(len(res)):
        cursor.execute("SELECT * FROM notations WHERE code = " + str(res[i]))
        row = cursor.fetchone()
        try:
            c=id_of_res.index(row[0])
        except ValueError:
            id_of_res.append(row[0])
            results.append(classes.notation(row[2], row[1], row[3]))
        print(row)

    cursor.close()

    conn.close()

    return results


if __name__ == '__main__':
    x1 = []
    # file = input("Введите названние файла:\n")
    x1 = fragmentParse.parseXML("error5.xml")
    res = []
    print("+fragment\n", x1)
    res = search(x1)
