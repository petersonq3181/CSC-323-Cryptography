import crypto

# point w/ order 8 on server's curve 
p = crypto.EccAlgPoint(curve=crypto.curve, 
    x=16349894185180983439102154383611486412, 
    y=224942997200586455214256137069604954919)

print(p)


