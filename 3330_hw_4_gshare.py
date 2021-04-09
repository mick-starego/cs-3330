
instructions = [
    [0x6, True],
    [0xf, False],
    [0x9, False],
    [0xf, False],
    [0x9, False],
    [0x6, True],
    [0x9, False],
    [0x6, True], 
    [0xf, True] 
]

GLOBAL_HIST = 0
BHT = [0 for i in range(8)]

def get_prediction(i):
    BHT_i = i ^ GLOBAL_HIST
    return BHT[BHT_i], BHT_i

def update_hist(result):
    global GLOBAL_HIST
    GLOBAL_HIST = (GLOBAL_HIST * 2) % 8
    if result:
        GLOBAL_HIST += 1

def update_branch(i, result):
    if BHT[i] != 3 and result:
        BHT[i] += 1
    elif BHT[i] != 0 and not result:
        BHT[i] -= 1

def main():
    total = 0
    correct = 0
    for i in range(10000):
        for instr in instructions:
            prediction, BHT_i = get_prediction(instr[0] % 8)
            if (prediction > 1 and instr[1]) or (prediction <= 1 and not instr[1]):
                correct += 1
            total += 1

            update_branch(BHT_i, instr[1])
            update_hist(instr[1])

    print(correct/total)

if __name__=="__main__":
    main()