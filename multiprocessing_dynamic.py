import multiprocessing as mp

#Myfunction
def processing_data(thread,inList,start,end,output):
    myOutlist = []
    for i in range(start,end):
        myOutlist.append([thread,inList[i],start,end,i])
    output.put(myOutlist)

if __name__ == '__main__':
    output = mp.Queue()
    myList = [i for i in range(10)]
    parallel = 5
    listLenght = len(myList)
    start = 0;chunk = listLenght//parallel
    processes = []

    for i in range(parallel):
        if i == parallel -1:
            end = listLenght
        else:
            end = start + chunk

        #run the process
        pr = mp.Process(target=processing_data, args=(i,myList,start,end,output))
        processes.append(pr)
        start = end

    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()

    # Get process results from the output queue
    results = []
    for p in processes:
        # print(output.get())
        results.extend(output.get())

    for row in  results:
        print(row)
