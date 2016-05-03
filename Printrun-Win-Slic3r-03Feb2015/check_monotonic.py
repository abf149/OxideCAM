f=open("cali.cal","r")

v_prev=-1
i=0
for l in f:
    v=float(l)
    if v<v_prev:
        print("BREAK from " + str(i-1) + " to " + str(i) + ":")
        print(str(v_prev))
        print(str(v))
    v_prev=v
    i=i+1
    
f.close()