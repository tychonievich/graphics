"""
Uses data from tables in 

Andrew Stockman, Donald MacLeod, Nancy Johnson (1993) "Spectral sensitivity of the human cones" *Journal of the Optical Society of America A*, 10(12) pp. 2491--2521

to plot pure wavelengths within the theoretical response triangle.
"""

data = '''
390 -3.2197 -3.2606 -1.9156 -3.5037 -3.5967 -2.1038
395 -2.7931 -2.8206 -1.5073 -3.0445 -3.1245 -1.6412
400 -2.4874 -2.5269 -1.2053 -2.6515 -2.7147 -1.2413
405 -2.1744 -2.1953 -0.8810 -2.3204 -2.3631 -0.8994
410 -1.9401 -1.9428 -0.6433 -2.0576 -2.0726 -0.6216
415 -1.7991 -1.7768 -0.4452 -1.8795 -1.8560 -0.4200
420 -1.6526 -1.5888 -0.2809 -1.7576 -1.6883 -0.2777
425 -1.5789 -1.4695 -0.1640 -1.6575 -1.5418 -0.1740
430 -1.5159 -1.3623 -0.0992 -1.5695 -1.4113 -0.0953
435 -1.4531 -1.2650 -0.0485 -1.4872 -1.2951 -0.0370
440 -1.3853 -1.1708 -0.0160 -1.4161 -1.1968 -0.0058
445 -1.3411 -1.1084 -0.0008 -1.3620 -1.1209 -0.0017
450 -1.3014 -1.0537 -0.0367 -1.3116 -1.0561 -0.0222
455 -1.2452 -0.9877 -0.0832 -1.2585 -0.9962 -0.0535
460 -1.1669 -0.9035 -0.1042 -1.1860 -0.9220 -0.0902
465 -1.0791 -0.8188 -0.1745 -1.1045 -0.8404 -0.1272
470 -0.9857 -0.7332 -0.2122 -1.0138 -0.7533 -0.1863
475 -0.9029 -0.6599 -0.3084 -0.9238 -0.6733 -0.2767
480 -0.8362 -0.6047 -0.4366 -0.8613 -0.6239 -0.4042
485 -0.7770 -0.5562 -0.5671 -0.7910 -0.5674 -0.5402
490 -0.6994 -0.4916 -0.6959 -0.7267 -0.5170 -0.6791
495 -0.6048 -0.4137 -0.8125 -0.6342 -0.4405 -0.8046
500 -0.5087 -0.3345 -0.9371 -0.5277 -0.3488 -0.9243
505 -0.4114 -0.2515 -1.0627 -0.4272 -0.2633 -1.0485
510 -0.3262 -0.1819 -1.2088 -0.3380 -0.1892 -1.2068
515 -0.2504 -0.1205 -1.3755 -0.2622 -0.1284 -1.3635
520 -0.1852 -0.0684 -1.5477 -0.1976 -0.0793 -1.5313
525 -0.1354 -0.0336 -1.7360 -0.1484 -0.0459 -1.7112
530 -0.0974 -0.0112 -1.9224 -0.1101 -0.0239 -1.8918
535 -0.0722 -0.0015 -2.1058 -0.0773 -0.0069 -2.0710
540 -0.0560 -0.0011 -2.2859 -0.0542 -0.0002 -2.2510
545 -0.0385 -0.0001 -2.4626 -0.0382 -0.0022 -2.4277
550 -0.0233 -0.0034 -2.6361 -0.0261 -0.0099 -2.6012
555 -0.0152 -0.0174 -2.8065 -0.0142 -0.0205 -2.7716
560 -0.0143 -0.0414 -2.9738 -0.0054 -0.0369 -2.9389
565 -0.0101 -0.0652 -3.1382 -0.0008 -0.0617 -3.1033
570 -0.0013 -0.0872 -3.2997 -0.0005 -0.0952 -3.2648
575 -0.0023 -0.1262 -3.4584 -0.0057 -0.1389 -3.4235
580 -0.0108 -0.1792 -3.6143 -0.0140 -0.1906 -3.5794
585 -0.0189 -0.2321 -3.7676 -0.0219 -0.2469 -3.7327
590 -0.0307 -0.2933 -3.9183 -0.0337 -0.3120 -3.8834
595 -0.0495 -0.3708 -4.0665 -0.0525 -0.3882 -4.0316
600 -0.0744 -0.4582 -4.2122 -0.0777 -0.4748 -4.1773
605 -0.1055 -0.5529 -4.3554 -0.1092 -0.5711 -4.3205
610 -0.1443 -0.6598 -4.4964 -0.1478 -0.6771 -4.4615
615 -0.1914 -0.7792 -4.6350 -0.1946 -0.7924 -4.6001
620 -0.2472 -0.9050 -4.7714 -0.2491 -0.9139 -4.7365
625 -0.3123 -1.0370 -4.9056 -0.3101 -1.0334 -4.8707
630 -0.3877 -1.1789 -5.0377 -0.3815 -1.1594 -5.0028
635 -0.4723 -1.3295 -5.1677 -0.4688 -1.3073 -5.1328
640 -0.5641 -1.4825 -5.2957 -0.5663 -1.4670 -5.2608
645 -0.6645 -1.6355 -5.4217 -0.6690 -1.6345 -5.3868
650 -0.7761 -1.7917 -5.5458 -0.7795 -1.8047 -5.5109
655 -0.8990 -1.9512 -5.6679 -0.8992 -1.9615 -5.6330
660 -1.0304 -2.1141 -5.7882 -1.0267 -2.1137 -5.7533
665 -1.1681 -2.2785 -5.9067 -1.1609 -2.2722 -5.8718
670 -1.3099 -2.4412 -6.0235 -1.3016 -2.4327 -5.9886
675 -1.4536 -2.5996 -6.1385 -1.4490 -2.5949 -6.1036
680 -1.5994 -2.7550 -6.2518 -1.6010 -2.7574 -6.2169
685 -1.7486 -2.9125 -6.3635 -1.7556 -2.9185 -6.3285
690 -1.9024 -3.0719 -6.4735 -1.9126 -3.0793 -6.4386
695 -2.0647 -3.2353 -6.5819 -2.0712 -3.2415 -6.5470
700 -2.2334 -3.4003 -6.6889 -2.2312 -3.4031 -6.6539
705 -2.4006 -3.5629 -6.7942 -2.3925 -3.5636 -6.7593
710 -2.5580 -3.7191 -6.8982 -2.5540 -3.7226 -6.8632
715 -2.7084 -3.8690 -7.0006 -2.7145 -3.8796 -6.9657
720 -2.8674 -4.0206 -7.1016 -2.8744 -4.0350 -7.0667
725 -3.0243 -4.1705 -7.2013 -3.0338 -4.1890 -7.1664
730 -3.1791 -4.3186 -7.2995 -3.1922 -4.3414 -7.2646
'''


def to_linear(srgb):
    '''convert single value from sRGB-gamma 0-1 to linear 0-1'''
    if srgb < 0.04045: return srgb / 12.92
    else: return ((srgb + 0.55) / 1.055)**2.4
def from_linear(linear):
    '''convert single value from linear 0-1 to sRGB-gamma 0-1'''
    if linear < 0.0031308: return linear * 12.92
    else: return 1.055 * (linear**(1/2.4)) - 0.055
def threecolor(r,g,b):
    '''given r,g,b in linear 0-1, return linear combination in sRGB as hex color string'''
    # lum = 1/max(r,g,b)
    # r,g,b = r*lum, g*lum, b*lum
    r,g,b = from_linear(r), from_linear(g), from_linear(b)
    r,g,b = round(255*r), round(255*g), round(255*b)
    return '#{:02X}{:02X}{:02X}'.format(r,g,b)

s,m,l = (0,100*3**.5), (100,0), (200,100*3**.5)
#s,m,l = (0,200), (-200,0), (100, 180)
dotsize = 2

with open('markdown/book/color-curve.svg', 'w') as f, open('markdown/book/color-area.svg', 'w') as f2, open('markdown/book/color-response.svg', 'w') as f3:
    print('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="385 -10 360 120">'.format(), file=f3)
    for fh in f,f2:
        print('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="{} {} {} {}">'.format(
                min(l[0],m[0],s[0])-dotsize,
                min(l[1],m[1],s[1])-dotsize,
                (max(l[0],m[0],s[0])-min(l[0],m[0],s[0]))+dotsize*2,
                (max(l[1],m[1],s[1])-min(l[1],m[1],s[1]))+dotsize*2,
            ), file=fh)
        print('<path d="M {} Z" stroke-width="{}" stroke="black" stroke-linejoin="round" fill="black"/>'.format(' '.join(str(_)[1:-1].replace(' ','') for _ in (l,m,s)), 2*dotsize), file=fh)
        print('<text x="{}" y="{}" fill="#ff8080" text-anchor="middle" font-family="arial" font-size="10px">L</text>'.format(l[0]-5,l[1]),file=fh)
        print('<text x="{}" y="{}" fill="#00ff00" text-anchor="middle" font-family="arial" font-size="10px">M</text>'.format(m[0],m[1]+10),file=fh)
        print('<text x="{}" y="{}" fill="#8080ff" text-anchor="middle" font-family="arial" font-size="10px">S</text>'.format(s[0]+5,s[1]),file=fh)
        lp = None
    sc,mc,lc = [],[],[]
    nmxy = {}
    for line in data.strip().split('\n'):
        nm,sbl,sbm,sbs,ciel,ciem,cies = line.split()
        nm = int(nm)
        lr0, mr0, sr0 = float(sbl), float(sbm), float(sbs)
        lr, mr, sr = (10**_ for _ in (lr0,mr0,sr0))
        sc.append((nm,100-sr*100))
        mc.append((nm,100-mr*100))
        lc.append((nm,100-lr*100))
        bright = int(min(1,(max(lr,mr,sr)+1/256))*255)
        color = '#'+('0'+hex(bright)[2:])[-2:]*3
        norm = lr+mr+sr
        x = (l[0]*lr + m[0]*mr + s[0]*sr)/norm
        y = (l[1]*lr + m[1]*mr + s[1]*sr)/norm
        nmxy[nm] = x,y
        if lp is not None:
            print('<line title="{}" stroke="{}" x1="{}" y1="{}" x2="{}" y2="{}" stroke-width="{}" stroke-linecap="round"/>'.format(str(nm)+'nm',color,lp[0],lp[1],x,y,dotsize), file=f)
        print('<circle title="{}" fill="white" cx="{}" cy="{}" r="{}"/>'.format(str(nm)+'nm',x,y,dotsize/2), file=f2)
        lp = (x,y)
    m93 = (3.1*nmxy[560][0] + 0.8*nmxy[500][0])/3.9, (3.1*nmxy[560][1] + 0.8*nmxy[500][1])/3.9
    s93 = (4*nmxy[390][0] + 0.8*nmxy[495][0])/4.8, (4*nmxy[390][1] + 0.8*nmxy[495][1])/4.8
    l93 = (7.6*nmxy[700][0] + 1.3*nmxy[515][0])/8.9, (7.6*nmxy[700][1] + 1.3*nmxy[515][1])/8.9
    
    print('<circle title="blue" fill="#0000FF" cx="{}" cy="{}" r="{}"/>'.format(s93[0],s93[1],dotsize), file=f)
    print('<circle title="green" fill="#00FF00" cx="{}" cy="{}" r="{}"/>'.format(m93[0],m93[1],dotsize), file=f)
    print('<circle title="red" fill="#FF0000" cx="{}" cy="{}" r="{}"/>'.format(l93[0],l93[1],dotsize), file=f)
    
    dots = 64
    for r in range(dots+1):
        for g in range(dots-r+1):
            b = dots-r-g
            print('<circle fill="{}" cx="{}" cy="{}" r="{}"/>'.format(
            threecolor(r/dots,g/dots,b/dots),
            (l93[0]*r+m93[0]*g+s93[0]*b)/dots,
            (l93[1]*r+m93[1]*g+s93[1]*b)/dots,
            dotsize*.6
            ), file=f)
            
    
    
    print('<path fill="none" stroke="blue" d="M{}"/>'.format(' '.join('{},{}'.format(*x) for x in sc)), file=f3)
    print('<path fill="none" stroke="green" d="M{}"/>'.format(' '.join('{},{}'.format(*x) for x in mc)), file=f3)
    print('<path fill="none" stroke="red" d="M{}"/>'.format(' '.join('{},{}'.format(*x) for x in lc)), file=f3)
    for fh in f,f2,f3:
        print('</svg>', file=fh)

