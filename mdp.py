

if __name__ == '__main__':
    Vg = 0
    Vb = 0
    Rgp = 0.8
    Rgi = 0
    Rbr = -2
    r = 0.9
    Pgbp = 0.2
    Pggp = 0.8
    Pggi = 1
    Pbgr = 0.8
    Pbbr = 0.2
    sign = 1
    while sign > 0:
        sign=abs(Rbr+r*(Pbgr*Vg+Pbbr*Vb)-Vb)
        Vb=Rbr+r*(Pbgr*Vg+Pbbr*Vb)
        Vg=max(Rgp+r*(Pgbp*Vb+Pggp*Vg),Rgi+r*(Pggi*Vg))
    print(Vg,Vb)
