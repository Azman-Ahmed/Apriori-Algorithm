class pattern:
    def __init__(self, iset, s):
        self.itemset = iset.copy()  # Ensure a proper copy of the list
        self.support = s

def joinable(itemset1, itemset2):
    return itemset1[:-1] == itemset2[:-1]

def downward_closure(itemset, Lk_minus_1):
    subsets = [itemset[:i] + itemset[i+1:] for i in range(len(itemset))]
    for subset in subsets:
        if subset not in [p.itemset for p in Lk_minus_1]:
            return False
    return True

path = "C:/Users/ASUS/Desktop/Jamai/Data/101.txt"

# Read the file into memory
with open(path, "r") as fptr:
    lines = fptr.readlines()

C = [[]]
L = [[]]
itemlist = []
n = 0

for line in lines:
    n += 1
    token = line.split()
    token.sort()
    print(f"Line {n}: {line.strip()}")
    print(f"Tokens: {token}")

    for item in token:
        temp = pattern([item], 1)
        flag = False

        for j in range(len(C[0])):
            if C[0][j].itemset == temp.itemset:
                C[0][j].support += 1
                flag = True
                break

        if not flag:
            C[0].append(temp)

min_support = n * 10 / 100

for i in range(len(C[0])):
    if C[0][i].support >= min_support:
        L[0].append(C[0][i])

print("Candidate")
for j in range(len(C[0])):
    print(f"Itemset: {C[0][j].itemset} Support: {C[0][j].support}")

print("Frequent")
for j in range(len(L[0])):
    print(f"Itemset: {L[0][j].itemset} Support: {L[0][j].support}")
    
k = 1
while True:
    C.append([])
    for i in range(len(L[k - 1])):
        for j in range(i + 1, len(L[k - 1])):
            itemset1 = L[k - 1][i].itemset
            itemset2 = L[k - 1][j].itemset

            if joinable(itemset1, itemset2):
                new_candidate = sorted(list(set(itemset1) | set(itemset2)))

                if downward_closure(new_candidate, L[k - 1]):
                    temp = pattern(new_candidate, 0)
                    C[k].append(temp)

    if len(C[k]) == 0:
        break

    for line in lines:
        token = line.split()
        token.sort()
        transaction_set = set(token)

        for i in range(len(C[k])):
            if set(C[k][i].itemset).issubset(transaction_set):
                C[k][i].support += 1

    L.append([])
    for i in range(len(C[k])):
        if C[k][i].support >= min_support:
            L[k].append(C[k][i])

    k += 1

print("Frequent Itemsets:")
for i in range(len(L)):
    for item in L[i]:
        print(f"Itemset: {item.itemset} Support: {item.support}")