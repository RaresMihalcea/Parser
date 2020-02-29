import pandas as pd
import numpy as np

d = pd.read_csv('./data.txt', sep=" ")

d = d.drop(['Index'], axis=1)

parents = d[['Parent']].to_numpy().flatten()
x = d[['X']].to_numpy().flatten()
y = d[['Y']].to_numpy().flatten()
z = d[['Z']].to_numpy().flatten()

class Branch:

    indexes = []

    def __init__(self, start_point):
        self.start_point = start_point
        self.end_point = start_point
        self.last_in_chain = start_point
        self.length = 0
        self.to_execute = None
        self.indexes.append(parents[start_point])
        self.run()

    def run(self):
        i = self.start_point + 1
        if i < len(parents):
            while parents[i] >= max(self.indexes):
                self.indexes.append(parents[i])
                a = np.array((x[i], y[i], z[i]))
                b = np.array((x[self.last_in_chain], y[self.last_in_chain], z[self.last_in_chain]))
                self.length += np.linalg.norm(a - b)
                self.end_point = parents[i]
                if i + 1 != len(parents):
                    i += 1
                else:
                    break

        if i < len(parents):
            self.to_execute = i

b_arr = []
b = Branch(parents[0])
b_arr.append(b)

for i in b_arr:
    while not i.to_execute == None:
        execute = i.to_execute
        i.to_execute = None
        b_arr.append(Branch(execute))

b_arr = b_arr[0:-1]

rel = []
for i in b_arr:
    # print(i.start_point, i.end_point)
    # print(parents[i.start_point])
    rel.append(parents[i.start_point])

matrix = []

for i in range(len(b_arr)):
    matrix.append([])
    for j in range(len(b_arr)):
        matrix[i].append(0)

j = 0
for i in b_arr:
    j += 1

# print(j)
# j = 0
# for i in range(len(b_arr)):

# print(parents[b_arr[1].start_point])
for i in range(len(b_arr)):
    start = parents[b_arr[i].start_point]
    for j in range(len(b_arr)):
        if i != j and start >= b_arr[j].start_point and start <= b_arr[j].end_point:
            matrix[i][j] = b_arr[i].length
            matrix[j][i] = b_arr[i].length
            
file1 = open("out.txt","w") 

for i in range(len(matrix)):
    out = ""
    for j in range(len(matrix)):
        out += str(matrix[i][j])
        if j < len(matrix) - 1:
            out += " "
    out += '\n'
    file1.write(out)
