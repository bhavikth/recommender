from csv import reader
cr = reader(open('recsys-data-WA 1 Rating Matrix.csv'))
rows=[]
for r in cr:
    rows+=[r]

movies_dict = {i-1:(rows[0][i].split(':')[0],rows[0][i].split(':')[1]) for i in range(1,21)}

cnt = [ len([ rows[i][j] for i in range(1,21) if rows[i][j] != '' ]) 
       for  j in range(1,21) ]
cnt_d={cnt[i]:movies_dict[i][0] for i in range(20)}
print([(i,cnt_d[i]) for i in reversed(sorted(cnt_d))])

cnt4 = [ len([ rows[i][j] for i in range(1,21) if rows[i][j] != '' and int(rows[i][j])>=4]) 
        for  j in range(1,21) ]
cnt4_d = {round(100*cnt4[i]/cnt[i],2):movies_dict[i][0] for i in range(0,20)}

print([(i,cnt4_d[i]) for i in reversed(sorted(cnt4_d))])

csum = [ sum([ int(rows[i][j]) for i in range(1,21) if rows[i][j] != '' ]) 
        for  j in range(1,21) ]


csum_d={round(csum[i]/cnt[i],2):movies_dict[i][0] for i in range(0,20)}
print([(i,csum_d[i]) for i in reversed(sorted(csum_d))])

x = 1
xy = [ len([ rows[i][y] for i in range(1,21) if rows[i][y] != '' and rows[i][x]!= '']) 
       for  y in range(1,21) ]
cx = len([1 for i in range(1,21) if rows[i][x] != ''])
xy_d=[ (movies_dict[i][0],round(100*xy[i]/cx,2)) for i in range(0,20)]
print(list(sorted(xy_d,key=lambda x:x[1],reverse=True)))



_xy = [ len([ rows[i][y] for i in range(1,21) if rows[i][y] != '' and rows[i][x]== '']) 
       for  y in range(1,21) ]

_x = len([ rows[i][x] for i in range(1,21) if rows[i][x] == '' ])