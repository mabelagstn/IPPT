from ippt import *
import csv

def read_csv(csvfilename):
    rows = ()
    with open(csvfilename) as csvfile:
        file_reader = csv.reader(csvfile)
        for row in file_reader:
            rows += (tuple(row), )
    return rows

def read_data(filename):
    rows = read_csv(filename)
    age_title = ()
    rep_title = ()
    data = ()
    for val in rows[0][1:]:
        rep_title += (int(val),)
 
    for row in rows[1:]:
        age_title += (int(row[0]),)
    
        row_data = ()
        for val in row[1:]:
            row_data += (int(val),)
        data += (row_data,)
    return create_table(data, age_title, rep_title)

pushup_table = read_data("pushup.csv")
situp_table = read_data("situp.csv")
run_table = read_data("run.csv")
ippt_table = make_ippt_table(pushup_table, situp_table, run_table)

def pushup_score(pushup_table, age, pushup):
    if pushup > 60:
        pushup = 60
    if pushup < 1:
        pushup = 1
    return access_cell(pushup_table, age, pushup)
    
def situp_score(situp_table, age, situp):
    if situp > 60:
        situp = 60
    if situp < 1:
        situp = 1
    return access_cell(situp_table, age, situp)

def run_score(run_table, age, run):
    while run % 10 != 0:
        run += 1
    if run > 1110:
        run = 1110
    elif run < 510:
        run = 510
    return access_cell(run_table, age, run)

# print(pushup_score(pushup_table, 18, 61))   # 25
# print(pushup_score(pushup_table, 18, 70))   # 25
# print(situp_score(situp_table, 24, 0))      # 0

# print(run_score(run_table, 30, 720))        # 36
# print(run_score(run_table, 30, 725))        # 35
# print(run_score(run_table, 30, 735))        # 35
# print(run_score(run_table, 30, 500))        # 50
# print(run_score(run_table, 30, 1300))       # 0

def ippt_award(score):
    if score < 51:
        return "F"
    elif score < 61:
        return "P"
    elif score < 75:
        return "P$"
    elif score < 85:
        return "S"
    else:
        return "G"

# print(ippt_award(50))     # F
# print(ippt_award(51))     # P
# print(ippt_award(61))     # P$
# print(ippt_award(75))     # S
# print(ippt_award(85))     # G

def ippt_results(ippt_table, age, pushup, situp, run):
    # (Total IPPT Score, IPPT Award String)
    p_score = pushup_score(get_pushup_table(ippt_table), age, pushup)
    s_score = situp_score(get_situp_table(ippt_table), age, situp)
    r_score = run_score(get_run_table(ippt_table), age, run)
    total = p_score + s_score + r_score
    award = ippt_award(total)
    return (total, award)

# print(ippt_results(ippt_table, 25, 30, 25, 820))      # (53, 'P')
# print(ippt_results(ippt_table, 28, 56, 60, 530))      # (99, 'G')
# print(ippt_results(ippt_table, 38, 18, 16, 950))      # (36, 'F')
# print(ippt_results(ippt_table, 25, 34, 35, 817))      # (61, 'P$')
# print(ippt_results(ippt_table, 60, 70, 65, 450))      # (100, 'G')

def parse_results(csvfilename):
    data = []
    stats = read_csv(csvfilename)
    data.append(tuple(stats[0]) + ("Total-Score", "Award"))
    
    for row in stats[1:]:
        name = row[0]
        age = int(row[1])
        pushup = int(row[2])
        situp = int(row[3])
        run = int(row[4])
        
        total, award = ippt_results(ippt_table, age, pushup, situp, run)
        data.append((name, age, pushup, situp, run, total, award))
    return data

ippt_takers_data = parse_results("ippt_takers_data.csv")
# print(ippt_takers_data[0])    # ('Name', 'Age', 'Push-Ups', 'Sit-Ups', '2.4-Km-Run', 'Total-Score', 'Award')
# print(ippt_takers_data[1])    # ('Sean Hendricks', 38, 25, 74, 1212, 42, 'F')
# print(ippt_takers_data[2])    # ('Phillip Brown DDS', 59, 15, 15, 852, 61, 'P$')
# print(ippt_takers_data[3])    # ('Ryan Gray MD', 24, 45, 78, 1074, 46, 'F')

def num_awards(ippt_takers_data, age):
    res = {}
    data = list(filter(lambda r : int(r[1]) == age, ippt_takers_data[1:]))
    for row in data:
        if row[-1] not in res:
            res[row[-1]] = 0
        res[row[-1]] += 1
    return res

# print(num_awards(ippt_takers_data, 25))    # {'F': 56, 'P': 20, 'G': 18, 'P$': 14, 'S': 10}
# print(num_awards(ippt_takers_data, 28))    # {'F': 54, 'S': 13, 'G': 16, 'P': 8, 'P$': 12}

def top_k_scores(ippt_takers_data, k, age):
    data = list(filter(lambda r : int(r[1]) == age, ippt_takers_data[1:]))
    res = {} # {name : total score}
    for row in data:
        name = row[0]
        age = int(row[1])
        pushup = int(row[2])
        situp = int(row[3])
        run = int(row[4])
        
        if name not in res:
            res[name] = 0
        res[name] += ippt_results(ippt_table, age, pushup, situp, run)[0]
        
    result = list(res.items())
    result.sort(key = lambda x : (-x[1], x[0]))
    while k < len(result) and result[k-1][1] == result[k][1]:
        k += 1 
    return result[:k]

# print(top_k_scores(ippt_takers_data, 5, 25))    # [('Joseph Burns', 100), ('Mike Williams', 98), ('Rachel Serrano', 98), ('Margaret Jennings', 97), ('Alexandra Day', 95), ('Stephen Boyer', 95)]
# print(top_k_scores(ippt_takers_data, 1, 28))    # [('Eric Villegas', 100), ('Melissa Evans', 100)]
# print(top_k_scores(ippt_takers_data, 2, 28))    # [('Eric Villegas', 100), ('Melissa Evans', 100)]
