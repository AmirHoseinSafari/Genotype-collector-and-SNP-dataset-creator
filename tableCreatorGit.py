import csv
import os


NumOfFiles = 100
NumOfThreads = 5

FILE_NAME = "FinalRes"
rowsArray = []
folderContent = os.listdir(FILE_NAME)
id = []
order = []
result = []
statsOfColumns = []
finalPos = []


def getFileNames():
    for i in range(0, len(folderContent)):
        if folderContent[i].__contains__("_table.csv"):
            id.append(folderContent[i][6:len(folderContent[i]) - 10])  # - 11])


# From: "https://www.geeksforgeeks.org/python-program-for-binary-search/"
def binarySearch(arr, l, r, x):
    # Check base case
    if r >= l:
        mid = l + (r - l) // 2
        if (len(arr) - 1 )< mid:
            return -1 * (len(arr))
        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

            # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binarySearch(arr, l, mid - 1, x)

            # Else the element can only be present in right subarray
        else:
            return binarySearch(arr, mid + 1, r, x)

    else:
        # Element is not present in the array
        return -1 * l

def commonPositions():
    order = []
    for ii in range(0, NumOfFiles):
        fileName = "Final_" + id[ii] + "_table.csv"
        with open(FILE_NAME + '/' + fileName, 'r') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                alts = dict(row).get('ALT')
                refs = dict(row).get('REF')
                poss = dict(row).get('POS')

                flag = -1
                if len(order) == 0:
                    flag = -2
                if flag != -2:
                    j = binarySearch(order, 0, len(order), int(poss))
                    if j > 0:
                        if j > 10:
                            for jj in range(j - 10, len(order)):
                                if int(poss) == order[jj]:
                                    if finalPos[jj] == (poss + ", " + refs + ", " + alts):
                                        flag = 0
                                        break
                                if int(poss) < order[jj]:
                                    break
                        else:
                            if int(poss) == order[j]:
                                if finalPos[j] == (poss + ", " + refs + ", " + alts):
                                    flag = 0
                        if flag == -1:
                            j = j * -1
                    if j == 0:
                        if order[0] == int(poss):
                            if finalPos[j] == (poss + ", " + refs + ", " + alts):
                                flag = 0
                                # break
                        if flag == -1:
                            flag = 0
                            order.insert(0, int(poss))
                            finalPos.insert(0, poss + ", " + refs + ", " + alts)
                    if j < 0:
                        j = -1 * j
                        if j > 50:
                            for kk in range((j - 15), len(order)):
                                if int(poss) == order[kk]:
                                    if finalPos[kk] == (poss + ", " + refs + ", " + alts):
                                        flag = 0
                                        break
                                if order[kk] > int(poss):
                                    if kk == 0:
                                        flag = 0
                                        order.insert(0, int(poss))
                                        finalPos.insert(0, poss + ", " + refs + ", " + alts)
                                    else:
                                        flag = 0
                                        order.insert(kk, int(poss))
                                        finalPos.insert(kk, poss + ", " + refs + ", " + alts)
                                    break
                        else:
                            for kk in range((j - 1), len(order)):
                                if order[kk] > int(poss):
                                    if kk == 0:
                                        flag = 0
                                        order.insert(0, int(poss))
                                        finalPos.insert(0, poss + ", " + refs + ", " + alts)
                                    else:
                                        flag = 0
                                        order.insert(kk, int(poss))
                                        finalPos.insert(kk, poss + ", " + refs + ", " + alts)
                                    break
                if flag == -2 or flag == -1:
                    order.append(int(poss))
                    finalPos.append(poss + ", " + refs + ", " + alts)
    print("total len: " + str(len(finalPos)))


def fillCell(ii):
    print(ii)
    fileName = "Final_" + id[ii] + "_table.csv"
    alts = []
    refs = []
    poss = []
    try:
        with open(FILE_NAME + '/' + fileName, 'r') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                alts.append(dict(row).get('ALT'))
                refs.append(dict(row).get('REF'))
                poss.append(dict(row).get('POS'))

            row = []
            row.append(id[ii])
            index = 0
            for i in range(0, len(finalPos)):
                if index == -1:
                    row.append(0)
                    continue
                if finalPos[i] == (poss[index] + ", " + refs[index] + ", " + alts[index]):
                    row.append(1)
                    index += 1
                    if index == len(poss):
                        index = -1
                else:
                    row.append(0)

            rowsArray.append(row)
    except:
        print("Error")
    # fileName = "Final_" + id[ii] + "_table.csv"
    # alts = []
    # refs = []
    # poss = []
    # a = 1
    # if a == 1:
    #      with open(FILE_NAME + '/' + fileName, 'r') as file:
    #         csv_file = csv.DictReader(file)
    #         for row in csv_file:
    #             alts.append(dict(row).get('ALT'))
    #             refs.append(dict(row).get('REF'))
    #             poss.append(dict(row).get('POS'))
    #
    #         row = []
    #         row.append(id[ii])
    #         index = 0
    #         for ii in range(0, len(poss)):
    #             flag = -1
    #             i = binarySearch(order, 0, len(order), poss[ii])
    #         # for i in range(0, len(finalPos)):
    #             if index == -1:
    #                 row.append(0)
    #                 continue
    #             if i > 0:
    #                 for j in range(i - 1, len(order)):
    #                     if finalPos[j] == (poss[index] + ", " + refs[index] + ", " + alts[index]):
    #                         row.append(1)
    #                         index += 1
    #                         flag = 1
    #                         if index == len(poss):
    #                             index = -1
    #             else:
    #                 for j in range(i, len(order)):
    #                     if finalPos[j] == (poss[index] + ", " + refs[index] + ", " + alts[index]):
    #                         row.append(1)
    #                         index += 1
    #                         flag = 1
    #                         if index == len(poss):
    #                             index = -1
    #                 if flag == -1:
    #                     row.append(0)
    #
    #         rowsArray.append(row)
    # # except:
    # #     print("Error")

def clearTable():
    ZeroColumns = []
    for j in range(1, len(result[0])):
        columnSum = 0
        for i in range(1, len(result)):
            columnSum += result[i][j]
        if columnSum == 0:
            ZeroColumns.append(j)
    for i in range(len(ZeroColumns) - 1, 0, -1):
        for j in range(0, len(result)):
            print(j)
            print(ZeroColumns[i])
            print("__________")
            del result[j][ZeroColumns[i]]

def makeTable():
    commonPositions()
    # pool = multiprocessing.Pool(processes=NumOfThreads)
    print(len(id))
    print(NumOfFiles)
    # pool.map(fillCell, (ii for ii in range(0, NumOfFiles)))
    for ii in range(0, NumOfFiles):
        fillCell(ii)
    finalPos.insert(0, 'name/ pos- ref- alt')
    result.append(finalPos)
    for i in range(0, len(rowsArray)):
        result.append(rowsArray[i])
    # clearTable()
    saveToFileAsCSV("outputsF.csv", result)


def getStats():
    print("Here stats begin")
    for j in range(1, len(result[0])):
        columnSum = 0
        for i in range(1, len(result)):
            columnSum += result[i][j]
        statsOfColumns.append(columnSum)

    f5 = 0
    t10 = 0
    f50 = 0
    t100 = 0
    f500 = 0
    t1000 = 0
    for i in range(0, len(statsOfColumns)):
        if statsOfColumns[i] < 5:
            f5 += 1
        elif statsOfColumns[i] < 10:
            t10 += 1
            f5 += 1
        elif statsOfColumns[i] < 50:
            f50 += 1
            t10 += 1
            f5 += 1
        elif statsOfColumns[i] < 100:
            t100 += 1
            f50 += 1
            t10 += 1
            f5 += 1
        elif statsOfColumns[i] < 500:
            f500 += 1
            t100 += 1
            f50 += 1
            t10 += 1
            f5 += 1
        elif statsOfColumns[i] < 1000:
            t1000 += 1
            f500 += 1
            t100 += 1
            f50 += 1
            t10 += 1
            f5 += 1

    print("1000: " + str(t1000))
    print("500: " + str(f500))
    print("100: " + str(t100))
    print("50: " + str(f50))
    print("10: " + str(t10))
    print("5: " + str(f5))

    saveToFileAsTXT("stats.txt", statsOfColumns)


def saveToFileAsCSV(fileName, listName):
    with open(fileName, "w") as f:
        writer = csv.writer(f)
        writer.writerows(listName)


def saveToFileAsTXT(fileName, listName):
    with open(fileName, 'w') as f:
        for item in listName:
            f.write("%s\n" % item)


if __name__ == '__main__':
    getFileNames()
    makeTable()
    getStats()
