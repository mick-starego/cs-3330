# The only collision is 000, and both of those branches are
# not taken. Therefore, this should be able to achieve
# perfect prediction at steady state.
# Expected BHT: [0, 0, 3, 0, 3, 3, 3, 0]
# Expected accuracy: 99.9%
instructions = [
    # LSB ^ GLOBAL_HIST = BHT index
    [0x6, True], # 110 ^ 011 = 101
    [0xf, False], # 111 ^ 111 = 111
    [0x9, False], # 001 ^ 110 = 000
    [0xf, False], # 111 ^ 100 = 011
    [0x9, False], # 001 ^ 000 = 001
    [0x6, True], # 110 ^ 000 = 110
    [0x9, False], # 001 ^ 001 = 000
    [0x6, True], # 110 ^ 010 = 100
    [0xf, True] # 111 ^ 101 = 010
]

GLOBAL_HIST = 0b000
BHT = [0b00, 0b00, 0b00, 0b00, 0b00, 0b00, 0b00, 0b00]

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