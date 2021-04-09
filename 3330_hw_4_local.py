# PHT index 0 should never change.
# At steady state:
# 0x6 -> always true
# 0xf -> FFT
# 0x9 -> always false
# Expected PHT: [00, 00, 11, (00 or 01 or 10)]
# Expected BHT: [(00 or 01), 00, 00, 11]
# Expected accuracy: ~88.9%
instructions = [
    [0x6, True], # 10
    [0xf, False], # 11
    [0x9, False], # 01
    [0xf, False], # 11
    [0x9, False], # 01
    [0x6, True], # 10
    [0x9, False], # 01
    [0x6, True], # 10
    [0xf, True] # 11 At steady state, this will always be predicted false
]

PHT = [0 for i in range(4)]
BHT = [0 for i in range(4)]

def get_prediction(i):
    return BHT[PHT[i]], PHT[i]
    

def update_pattern(i, result):
    PHT[i] = (PHT[i] * 2) % 4
    if result:
        PHT[i] += 1

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
            prediction, BHT_i = get_prediction(instr[0] % 4)
            if (prediction > 1 and instr[1]) or (prediction <= 1 and not instr[1]):
                correct += 1
            total += 1

            update_branch(BHT_i, instr[1])
            update_pattern(instr[0] % 4, instr[1])
    
    print(correct/total)

if __name__=="__main__":
    main()