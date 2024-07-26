f = open('./../lastID.txt', 'r')
#read current id, and add 1
lastID = int(f.read()) + 1
f.close()
#write new id
f = open('./../lastID.txt', 'w')
f.write(str(lastID))
f.close()