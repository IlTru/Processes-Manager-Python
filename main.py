import random
from queue import Queue

class Process:
    def __init__(self, start, delta):
        self.start = start
        self.delta = delta

queueOfProcesses = Queue() #coada in care vom insera procesele

TS = 1000000 #cate unitati de timp va dura simularea
q = 80 #cate unitati de timp are o quanta
r_min=560 #distanza minima/maxima in unitati de timp intre un proces si urmatorul care va fi generat
r_max=1000
delta_min=60 #timpul minim/maxim de care are nevoie un proces sa-si termine task-ul
delta_max=1500

# variabile folosite pentru afisarea informatiilor
maxQueueSize = 0 #numarul maxim de procese pe care le-a avut coada la un moment dat
averageQueueSize = 0 #in medie cate procese a avut coada
numberOfProcesses = 0
averageDelta = 0

debug = False #afiseaza informatii la fiecare unitate de timp
info_queue = True #afiseaza informatii despre coada de procese
info_processes = True #afiseaza informatii despre procesele generate

listOfProcesses = []
listOfProcesses.append(Process(random.randint(r_min, r_max), random.randint(delta_min, delta_max))) #crearea primului element din lista de procese pentru simulator

while(listOfProcesses[len(listOfProcesses)-1].start<TS): #crearea listei
    numberOfProcesses = numberOfProcesses+1
    listOfProcesses.append(Process(listOfProcesses[len(listOfProcesses)-1].start + random.randint(r_min, r_max), random.randint(delta_min, delta_max)))

if info_processes:
    print("Generated processes:")
    for process in listOfProcesses: #afisare informaii despre procesele generate
        print(f"{process} : start={process.start} delta={process.delta}")

processInRunning = None #variabila care ne memoreaza procesul in rulare, aceasta este None daca procesorul este liber
indexNextProcess = 0 #index in care retin care este urmatorul proces care trebuie sa fie inserat in coada

for i in range(TS+1):
    if debug:
        if processInRunning != None:
            print(f"{i} Process in running: {processInRunning} with delta: {processInRunning.delta}")
        else:
            print(i)

    if i%q==0: #cand este adevarata aceasta conditie inseamna ca suntem la quanta
        if processInRunning:
            queueOfProcesses.put(processInRunning) #daca exista un proces in rulare in punem in coada
            if maxQueueSize < queueOfProcesses.qsize(): #coada se modifica si verific daca este la o valoare maxima (nu este valoarea maxima pe care o poate avea lungimea cozii ci valoarea maxima pe care a avut-o la un moment dat)
                maxQueueSize = queueOfProcesses.qsize()
            processInRunning = None #in acest moment nu avem un proces in rulare
        if queueOfProcesses.empty() == False:
            processInRunning = queueOfProcesses.get() #daca coada nu este goala extragem primul element din aceasta si in punem in rulare

    if processInRunning:
        if processInRunning.delta != 0:
            processInRunning.delta = processInRunning.delta - 1 #daca avem un proces in rulare cu delta-ul > 0 atunci scadem o unitate de timp la fiecare pas
        else:
            if debug: print(f"Process {processInRunning} has finished his tasks at time: {i}") #delta-ul a ajuns la 0 ceea ce inseamna ca procesul si-a terminat task-ul, acesta va fi scos din rulare iar urmatorul proces din coada va deveni noul proces in running
            processInRunning = None
            if queueOfProcesses.empty() == False:
                processInRunning = queueOfProcesses.get()

    if listOfProcesses[indexNextProcess].start == i: #verificam daca trebuie adaugat un nou proces in coada
        queueOfProcesses.put(listOfProcesses[indexNextProcess])
        if debug: print(f"Process {listOfProcesses[indexNextProcess]} added to queue")
        averageDelta = averageDelta + listOfProcesses[indexNextProcess].delta
        if processInRunning == None:
            processInRunning = queueOfProcesses.get()
        indexNextProcess = indexNextProcess + 1

    averageQueueSize = averageQueueSize + queueOfProcesses.qsize()

if info_queue: #afisez informatii despre coada
    print(f"Max Queue Size:{maxQueueSize}")
    averageQueueSize = "{:.2f}".format(averageQueueSize/TS)
    print(f"Average Queue Size:{averageQueueSize}")

if info_processes: #afisez informatii despre procese
    print(f"Number of processes that haven't completed their tasks:{queueOfProcesses.qsize()}")
    print(f"Total number of processes:{numberOfProcesses}")
    averageDelta = "{:.2f}".format(averageDelta/numberOfProcesses)
    print(f"Average Delta:{averageDelta}")