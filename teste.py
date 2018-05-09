a = [('SE', 'FI'), ('DK', 'SE')]
b = [['NL', 'DK', 0], ['NL', 'DE', 0], ['NL', 'BE', 10], ['SE', 'DK', 0], ['FI', 'SE', 0.054]]
founds = []
for val1, val2, val3 in b:
    if((val1, val2) in a):
        founds.append([val1, val2, val3])
    else:
        if ((val2, val1) in a):
            founds.append([val1, val2, val3])
print(founds)