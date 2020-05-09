def deleteTails(x, y):
    if x[0].isCommon:
        print(1)
        while not y[0].isCommon:
            del y[0]
    elif y[0].isCommon:
        print(2)
        while not x[0].isCommon:
            del x[0]
    lastx = len(x) - 1
    lasty = len(y) - 1
    if x[lastx].isCommon:
        print(3)
        while not y[lasty].isCommon:
            del y[lasty]
            lasty -= 1
    elif y[lasty].isCommon:
        print(4)
        while not x[lastx].isCommon:
            del x[lastx]
            lastx -= 1
    while not x[lastx].isNote:
        del x[lastx]
        lastx -= 1
    while not y[lasty].isNote:
        del y[lasty]
        lasty -= 1


def firstRule(x):
    N = 0
    i = 0
    common = False
    if not x[0].isCommon and not x[0].isNote and x[0].weight == 1 and not x[1].isCommon:
        if not x[1].isNote:
            j = 2
            while j < len(x):
                if x[j].isNote:
                    if x[j].isCommon:
                        common = True
                    else:
                        x[j].weight /= 2
                    break
                else:
                    j += 1
        if not common:
            print("1 в начале")
            x[1].weight /= 2
            del x[0]
            N += 1

    common = False
    while i < len(x) - 1:
        if not x[i].isCommon and not x[i + 1].isCommon and not x[i + 1].isNote and x[i + 1].weight == 1:
            if i + 2 < len(x):
                if not x[i + 2].isCommon:
                    if not x[i + 2].isNote:
                        j = i + 3
                        while j < len(x):
                            if x[j].isNote:
                                if x[j].isCommon:
                                    common = True
                                else:
                                    x[j].weight /= 2
                                break
                            else:
                                j += 1
                    if common:
                        break
                    x[i + 2].weight /= 2
                else:
                    break
            print(1)
            x[i].weight *= 2
            del x[i + 1]
            N += 1
        i += 1
    return N


def secondRule(x):
    N = 0
    i = 0
    common = False
    if not x[0].isCommon and not x[1].isCommon and not x[2].isCommon:
        if x[0].weight == x[1].weight == 1 and x[0].isNote and x[1].isNote:
            if (x[0].high == 1 and x[1].high == -1) or (x[0].high == -1 and x[1].high == 1):
                if not x[2].isNote:
                    j = 3
                    while j < len(x):
                        if x[j].isNote:
                            if x[j].isCommon:
                                common = True
                            else:
                                x[j].weight /= 3
                            break
                        else:
                            j += 1
                if not common:
                    print("2 в начале")
                    x[2].weight /= 3
                    del x[0]
                    del x[1]
                    N += 1

    common = False
    while i < len(x) - 2:
        if not x[i].isCommon and not x[i + 1].isCommon and not x[i + 2].isCommon and x[i + 1].weight == x[i + 2].weight == 1:
            if x[i].isNote and x[i + 1].isNote and x[i + 2].isNote:
                if (x[i + 1].high == 1 and x[i + 2].high == -1) or (x[i + 1].high == -1 and x[i + 2].high == 1):
                    print(2)
                    if i + 3 < len(x):
                        if not x[i + 3].isCommon:
                            if not x[i + 3].isNote:
                                j = i + 4
                                while j < len(x):
                                    if x[j].isNote:
                                        if x[j].isCommon:
                                            common = True
                                        else:
                                            x[j].weight /= 3
                                        break
                                    else:
                                        j += 1
                            if common:
                                break
                            x[i + 3].weight /= 3
                        else:
                            break
                    x[i].weight *= 3
                    del x[i + 1]
                    del x[i + 1]
                    N += 1
        i += 1

    return N


def thirdRule(x):
    N = 0
    i = 0
    if not x[0].isCommon and not x[1].isCommon and not x[2].isCommon and not x[3].isCommon:
        if x[0].weight == x[1].weight == x[2].weight == 1:
            if x[0].isNote and x[1].isNote and x[2].isNote:
                if (x[0].high == 1 and x[1].high == -2 and x[2].hign == 1) or \
                        x[0].high == -1 and x[1].high == 2 and x[2].hign == -1:
                    if not x[3].isNote:
                        j = 4
                        while j < len(x):
                            if x[j].isNote:
                                if x[j].isCommon:
                                    common = True
                                else:
                                    x[j].weight /= 4
                                break
                            else:
                                j += 1
                    if not common:
                        print("3 в начале")
                        x[3].weight /= 4
                        del x[0]
                        del x[1]
                        del x[2]
                        N += 1
    common = False
    while i < len(x) - 3:
        if not x[i].isCommon and not x[i + 1].isCommon and not x[i + 2].isCommon and not x[i + 3].isCommon:
            if x[i + 1].weight == x[i + 2].weight == x[i + 3].weight == 1:
                if x[i].isNote and x[i + 1].isNote and x[i + 2].isNote and x[i + 3].isNote:
                    if (x[i + 1].high == 1 and x[i + 2].high == -2 and x[i + 3].hign == 1) or \
                            x[i + 1].high == -1 and x[i + 2].high == 2 and x[i + 3].hign == -1:
                        print(3)
                        if i + 4 < len(x):
                            if not x[i + 4].isCommon:
                                if not x[i + 4].isNote:
                                    j = i + 5
                                    while j < len(x):
                                        if x[j].isNote:
                                            if x[j].isCommon:
                                                common = True
                                            else:
                                                x[j].weight /= 4
                                            break
                                        else:
                                            j += 1
                                if common:
                                    break
                                x[i + 4].weight /= 4
                            else:
                                break
                        x[i].weight *= 4
                        del x[i + 1]
                        del x[i + 1]
                        del x[i + 1]
                        N += 1
        i += 1
    return N

                                                                     
def correctMistakes(x, y):
    N = 0
    if not x[0].isCommon and x[1].isCommon and x[0].isNote:
        if not y[0].isCommon and y[1].isCommon and y[0].weight == x[0].weight and y[0].isNote:
            if abs(y[0].high - x[0].high) == 1:
                y[0].high = x[0].high
                N += 1
        else:
            for j in range(0, len(y) - 2):
                if not y[j].isCommon and not y[j + 1].isCommon and y[j + 2].isCommon and y[j + 1].weight == x[0].weight and \
                        y[j].isNote and y[j + 1].isNote:
                    if abs(y[j + 1].high - x[0].high) == 1:
                        y[j].high += x[0].high - y[j + 1].high
                        y[j + 1].high = x[0].high
                        N += 1
                        break

    for i in range(0, len(x) - 2):
        if not x[i].isCommon and not x[i + 1].isCommon and x[i + 2].isCommon and x[i].isNote and x[i + 1].isNote:
            for j in range(0, len(y) - 2):
                if not y[j].isCommon and not y[j + 1].isCommon and y[j + 2].isCommon and y[j + 1].weight == x[i + 1].weight and y[j].isNote and y[j + 1].isNote:
                    if abs(y[j + 1].high - x[i + 1].high) == 1:
                        y[j].high += x[i + 1].high - y[j + 1].high
                        y[j + 1].high = x[i + 1].high
                        N += 1
                        break

    for i in range(0, len(x) - 1):
        if x[i].isCommon and not x[i + 1].isCommon and x[i].isNote and x[i + 1].isNote:
            for j in range(0, len(y) - 1):
                if y[j].isCommon and not y[j + 1].isCommon and y[j].isNote and y[j + 1].isNote and y[j + 1].weight == x[i + 1].weight:
                    if abs(y[j + 1].high - x[i + 1].high) == 1:
                        if j + 2 < len(y):
                            y[j + 2].high -= x[i + 1].high - y[j + 1].high
                        y[j + 1].high = x[i + 1].high
                        N += 1

    return N


def finale(x, y):
    wavesedges_x = []
    wavesedges_y = []
    N = 0
    for i in range(1, len(x) - 1):
        if x[i].isCommon and not x[i + 1].isCommon:
            wavesedges_x.append(i)
        if x[i + 1].isCommon and not x[i].isCommon:
            wavesedges_x.append(i + 1)
    for i in range(1, len(y) - 1):
        if y[i].isCommon and not y[i + 1].isCommon:
            wavesedges_y.append(i)
        if y[i + 1].isCommon and not y[i].isCommon:
            wavesedges_y.append(i + 1)
    for i in range(len(wavesedges_x - 1)):
        local_x = []
        for j in range(wavesedges_x[i] + 1, wavesedges_x[i + 1]):
            print()
