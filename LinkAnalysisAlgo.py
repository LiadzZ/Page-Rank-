"""
Page_Rank_Link_Analysis


"""




import pickle  
import networkx as nx
import numpy
import matplotlib.pyplot as plt
from tkinter import messagebox
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from urllib.request import urlopen
import os
from urllib.parse import urlparse




class Page_Rank_Link_Analysis:

    def __init__(self):
        self.title = "PageRank algorithm"
        self.root = tk.Tk()
        self.root.title(self.title)
        w = 390  # width for the Tk root
        h = 220  # height for the Tk root

        # get screen width and height
        ws = self.root.winfo_screenwidth()  # width of the screen
        hs = self.root.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.frame = Frame(self.root)
        self.frame.grid()
        self.path = None
        self.newWebsite = Entry(self.root)
        self.flag_pickle = False
        self.numberOfitterations = 1
        self.link_Dic = {}
        self.page_rank_vector = {}
        self.temp_link_Dic = {}
        self.directiory = None
    def start(self):
        text = tk.Label(self.root, text="Click 'Browse' and choose whice website you want to rank:")
        text.grid(row=0, column=1)
        browseButton = Button(command=self.Path, text="Browse", fg="black")
        browseButton.grid(row = 1, column=1)


        text2 = tk.Label(self.root, text="Enter new website(url):")
        text2.grid(row=2, column=1)
        self.newWebsite.grid(row=3, column=1)

        text3 = tk.Label(self.root,text = "Start Data-Analysis")
        text3.grid(row=4,column=1)
        buildButton = Button(command=self.Build, text="Build", fg="black")
        buildButton.grid(row=5, column=1)


        pageRankButton = Button(command=self.PageRank, text="PageRank", fg="black")
        pageRankButton.grid(row=6, column=1)
        self.root.mainloop()
    def Path(self):
        file_path = tk.filedialog.askdirectory()
        self.path = file_path + "/LinkAnalysis.pkl"
        self.flag_pickle = True
        pass
    def Build(self):

        def fixAddress(list):
            list2 = []
            for address in list:
                if (address.startswith("http")):
                    list2.append(address)
                    
                else:
                    temp = add_http + address
                    address = temp
                    list2.append(address)
            return list2



        def removeUnwanted(source_Code):
            tempList = []
            for x in source_Code:
                if "http:" in x:
                    temp = x[x.find("http:"):]
                    temp = list(temp.split(chr(34)))
                    temp = list(temp[0].split(chr(39)))
                    if not (temp[0].endswith(";")):
                        tempList.append(temp[0])
                elif "www" in x:
                    temp = x[x.find('www'):]
                    temp = list(temp.split(chr(34)))
                    temp = list(temp[0].split(chr(39)))
                    if not (temp[0].endswith(";")):
                        tempList.append(temp[0])

                elif "https:" in x:
                    temp = x[x.find("https:"):]
                    temp = list(temp.split(chr(34)))
                    temp = list(temp[0].split(chr(39)))
                    if not (temp[0].endswith(";")):
                        tempList.append(temp[0])


            return fixAddress(tempList)

        def cleanAddress(Address):  # http://www.walla.co.il
            list1 = Address.split("/")
            return "http://" + list1[2]

        def itterFunc(address_test):
            numberOfErrors = 0
            allowedCounter = 0

            for x in address_test:
                temp_link = urlparse(x)

                  # dead end solution
                if temp_link.netloc != full_link:
                    continue

                if x in dictionary:
                    if (dictionary[x][2] == "GREEN"):
                        print("Already Visited - ", x)
                        continue

                try:
                    html = urlopen(x)
                except Exception as e:
                    numberOfErrors += 1
                    continue
                try:
                    content = html.read().decode()
                except Exception as e:
                    numberOfErrors += 1
                    continue
                allowedCounter += 1

                tempSTR = ""
                for k in content:
                    tempSTR += k
                tempList2 = list(tempSTR.split())
                innerAddresses = removeUnwanted(tempList2)
                innerAddresses = (list(set(innerAddresses)))

                for y in innerAddresses:
                    try:
                        new_link = urlparse(y)
                    except ValueError as e:
                        continue
                    if y in dictionary:
                        dictionary[y][0] = dictionary[y][0] + 1
                        dictionary[y][3].append(x)  # add to list-in
                    else:
                        if new_link.netloc == full_link:  # add to dict
                            dictionary[y] = [1, 0, "RED", [x], []]
                        else:                                                                      # add external website to dict
                            other_website = new_link.scheme +"://"+ new_link.netloc
                            if other_website in dictionary:
                                dictionary[other_website][0] = dictionary[other_website][0] + 1
                                dictionary[other_website][3].append(x)  # add to list-in
                            else:
                                dictionary[other_website] = [1, 0, "RED", [x], []]

                dictionary[x][1] = len(innerAddresses)
                dictionary[x][2] = "GREEN"
                dictionary[x][4] = innerAddresses

        messagebox._show("Program", "Building data base...this may take a while...")

        self.flag_pickle = False
        myAddress = str(self.newWebsite.get())
        LinkName2 = str(self.newWebsite.get())
        full_link = LinkName2.split('//')[1]

        try:

            html = urlopen(myAddress)
        except Exception as e:
            messagebox.showerror(title="Error", message="illegal address,try again..")
            pass
        try:
            content = html.read().decode()
        except Exception as e:
            messagebox.showerror(title="Error", message="Something went wrong.." + e)
            pass
        tempSTR = ""
        for x in content:
            tempSTR += x
        
        tempList = list(tempSTR.split())

        add_http = "http://"
        add_https = "https://"
        address_test = removeUnwanted(tempList)
        address_test.append(myAddress)

        address_test = (list(set(address_test)))  # remove duplicates

        dictionary = {}  ##      dictionary - [ IN , OUT , STATUS(GREEN - Already visited , RED - Not Visited) , LISTIN , LISTOUT ]

        for x in address_test:   # enter the first list of links to the dict..
            temp_link = urlparse(x)
            if full_link == temp_link.netloc:  # legit  netloc    (example: wwww.ynet.co.il )
                dictionary[x] = [1, 0, "RED", [myAddress], []]
            else:                              # other website
                other_website = temp_link.scheme + "://" + temp_link.netloc
                if other_website not in dictionary:
                    dictionary[other_website] = [1, 0, "RED", [myAddress], []]
        dictionary[myAddress] = [1, len(address_test), "GREEN", [], address_test] # add the user input website to the dict..

        itterFunc(address_test)

        for _ in range (self.numberOfitterations):
            tmpDict = {}
            for link in dictionary:
                tmpDict[link] = dictionary[link]
                
            tmplist = tmpDict.keys()
            itterFunc(tmplist)

        self.temp_link_Dic = dictionary

        messagebox.showinfo(title="Success",message="The build of the data structure succeeded")
        messagebox.showinfo(title="Pickle output", message="Saving the data structure to pickle file.")

        LinkName=str(self.newWebsite.get())

        tempoLink=LinkName.split('.')
        LinkName=tempoLink[1]

        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, LinkName)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)


        filename=LinkName+"/"+ "LinkAnalysis.pkl"
        dictionary["mainSite"] = full_link
        output = open(filename, "wb")
        pickle.dump(dictionary, output)
        output.close


        pass
       
    def PageRank(self):
        messagebox._show("Program","Running...this may take a few moments...")
        def removeNodes(dict2):
            link_Dic2 = {}
            for x in dict2:
               
                if x.endswith("pdf") or x.endswith("JPEG") or x.endswith("png") or x.endswith("jpg") or x.endswith("footer"):
                    continue

                link_Dic2[x] = dict2[x]
            return link_Dic2

        def probability_x_to_y(linkRow, linkCol):  # get the probability for the transition matrix
            if linkCol not in self.link_Dic[linkRow][3]:
                return 0
            divNum = 1 / self.link_Dic[linkCol][1]
            return divNum

        def transition_matrix_input(keyList, matrix, probability_x_to_y):
            for row in range(len(keyList)):
                for col in range(len(keyList)):
                    matrix[row][col] = probability_x_to_y(keyList[row], keyList[col])  # transition matrix input

        if self.flag_pickle is True:
            filename = self.path
            with open(filename, 'rb') as f:
                # The protocol version used is detected automatically, so we do not
                # have to specify it.
                self.temp_link_Dic = pickle.load(f)
            self.newWebsite = self.temp_link_Dic["mainSite"]

            del self.temp_link_Dic["mainSite"]

        else:
            if not self.temp_link_Dic:
                messagebox.showerror(title="Error",message="Browse or Enter new url first")
            else:
                self.newWebsite = self.temp_link_Dic["mainSite"]
                del self.temp_link_Dic["mainSite"]
                pass

        self.link_Dic = removeNodes(self.temp_link_Dic)  ##  [ IN , OUT , STATUS(GREEN - Already visited , RED - Not Visited) , LISTIN , LISTOUT ]
        numberDic = {}

        index = 1
        for key in self.link_Dic:  ## set dictionary with running index for our Graph input.
            print(key,"  ",self.link_Dic[key])
            numberDic[key] = index
            index += 1
        matrix = numpy.zeros(shape=(len(self.link_Dic), len(self.link_Dic)))  # Build NxN matrix ( N = number of links )

        key_list = []
        for key in self.link_Dic.keys():
            key_list.append(key)
            # this way we have no 'dict_keys' at the start

        transition_matrix_input(key_list, matrix, probability_x_to_y)
        sum_vector = {}
        multiply_vector = {}

        for link in key_list:  # represent vectors with dictionary
            multiply_vector[link] = 1  # our first vector initialize to 1
            sum_vector[link] = 0  # our sum vector

        sum_matrix = 0

        for _ in range(50):  # iterate Random walks
            index1 = 0  # our x in the matrix
            for x in key_list:
                index2 = 0  # our y in the matrix
                for y in key_list:
                    sum_matrix = sum_matrix + (matrix[index1][index2] * multiply_vector[y])
                    index2 += 1
                sum_vector[x] = (sum_matrix * 0.8) + 0.2  # avoid spider trap with 20% tax.
                sum_matrix = 0
                index1 += 1
            for k in sum_vector:
                multiply_vector[k] = sum_vector[k]  # our new multiply vector.

        maximum = max(multiply_vector.values())  # our highest page rank

        minimum = min(multiply_vector.values())  # out lowest page rank




        for link in multiply_vector:  # The Vector dictionary after normalization
            self.page_rank_vector[link] = (multiply_vector[link] - minimum) / (maximum - minimum)

        def mergeSort(arr):
            if len(arr) > 1:
                mid = len(arr) // 2  # Finding the mid of the array
                left = arr[:mid]  # Dividing the array elements
                right = arr[mid:]  # into 2 halves

                mergeSort(left)  # Sorting the first half
                mergeSort(right)  # Sorting the second half

                i = j = k = 0

                # Copy the data to temp lists left[] and right[]
                while i < len(left) and j < len(right):
                    if left[i][1] < right[j][1]:
                        arr[k] = left[i]
                        i += 1
                    else:
                        arr[k] = right[j]
                        j += 1
                    k += 1

                # Checking if any element was left
                while i < len(left):
                    arr[k] = left[i]
                    i += 1
                    k += 1

                while j < len(right):
                    arr[k] = right[j]
                    j += 1
                    k += 1

        rankList = []
        for x in self.page_rank_vector:
            rankList.append([x, self.page_rank_vector[x]])  # set list of our page rank [ link , pageRank(float) ]

        mergeSort(rankList)  # sort the list


        print("website: ", self.newWebsite)

        temp = self.newWebsite.split(".")
        LinkName = temp[1]
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, LinkName)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)



        # ---------------------- write to file 1------------------------
        i = len(rankList) - 1
        myPath = os.path.join(  LinkName , 'output1.txt')
        with open(myPath, 'w',encoding="utf-8") as f:  # write the result to file  [ linkName(str) , pageRank(float) ]
            for _ in range(len(rankList)):
                f.write(rankList[i][0] + "  ")
                f.write(str(rankList[i][1]) + '\n')
                i -= 1
                if (i < 0):
                    break


            messagebox.showinfo(title="Success",message="You can find the result(output1.txt) at the project library at: "+LinkName)
        f.close()
        # ---------------------- write to file 1 end------------------------
        # ---------------------- write to file 2------------------------
        i = len(rankList) - 1
        myPath = os.path.join(  LinkName , 'output2.txt')
        with open(myPath, 'w',encoding="utf-8") as f:  # write the result to file  [ linkName(str) , pageRank(float) ]
            for _ in range(len(rankList)):
                temp_address = urlparse(rankList[i][0])
                if temp_address.netloc == self.newWebsite:
                    f.write(rankList[i][0] + "  ")
                    f.write(str(rankList[i][1]) + '\n')
                i -= 1
                if (i < 0):
                    break
               

            messagebox.showinfo(title="Success", message="You can find the result(output2.txt) at the project library at: "+LinkName)
        f.close()
        # ---------------------- write to file 2 end------------------------

        if messagebox.askquestion(title=None,message = "Would you like to draw the graph?") == 'yes':
            messagebox.showinfo(title="Graph Drawing",message="Drawing...this may take a few moments...")
            # ---------------------- draw to Graph ------------------------
            blueCounter = 0
            redCounter = 0
            color_map = []
            node_size_map = []
            for node in key_list:
                if self.page_rank_vector[node] == 1:
                    color_map.append("red")
                    redCounter += 1
                    node_size_map.append(30)
                else:
                    color_map.append("blue")
                    node_size_map.append(10)
                    blueCounter += 1

            G = nx.Graph()
            nodeCounter = 0
            edgeCounter = 0
            for xx in numberDic:
                G.add_node(numberDic[xx])
                nodeCounter += 1
            for link in key_list:
                if link not in numberDic:
                    continue
                for outLink in self.link_Dic[link][3]:
                    if outLink not in numberDic:
                        continue
                    if (G.has_edge(numberDic[link], numberDic[outLink]) or G.has_edge(numberDic[outLink],
                                                                                      numberDic[link])):
                        continue
                    else:
                        G.add_edge(numberDic[link], numberDic[outLink], weight=1)
                        edgeCounter += 1

            options = {
                # 'node_color': 'black',
                # 'node_size': 20,
                'line_color': 'grey',
                'linewidths': 0,
                'width': 0.1,
                'edgelist': None,
                'edge_color': 'grey',
                'style': 'solid',
                'alpha': 1.0,
                'arrowstyle': '-|>',
                'arrowsize': 10,
                'edge_cmap': None,
                'edge_vmin': None,
                'edge_vmax': None,
                'ax': None,
                'arrows': True,
                'label': None,
                'nodelist': None,
                'node_shape': "o",

            }

            #pos = nx.random_layout(G)
            print("nodeCounter ", nodeCounter)
            print("edgeCounter ", edgeCounter)
            print("red(Strong) : ", redCounter)
            print("blue(Weeker) : ", blueCounter)


            nx.draw(G,node_color=color_map, node_size=node_size_map, **options)
            plt.figure(num=None, figsize=(1000, 1000), dpi=1)
            # plt.figure(num=None, figsize=(10,10) , dpi=1200)
            plt.axis('off')





            plt.show()
            self.link_Dic = {}
            self.page_rank_vector = {}
            self.temp_link_Dic = {}

        messagebox._show("Graph", "The drawing is finished")
        pass



def main():
    program = Page_Rank_Link_Analysis()
    program.start()



main()
