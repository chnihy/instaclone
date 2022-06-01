import pickle
emp = {1:"A",2:"B",3:"C",4:"D",5:"E"}
pickling_on = open("Emp.pickle","wb")
pickle.dump(emp, pickling_on)
pickling_on.close()

pickle_off = open("Emp.pickle","rb")
emp = pickle.load(pickle_off)
print(emp)