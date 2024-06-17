import sys
sys.setrecursionlimit(10**6)


##############Code for RBTREEE, as we require a Binary search tree#########################################

class Node:
    def __init__(self,v):
        self.value = v
        self.left  = None
        self.right = None
        self.parent = None
        self.size = 1
        self.color = "RED"

class RedBlackTree:

    def __init__(self):
        self.root = None

    def left_rotate(self,v):
        y = v.right
        v.right  = y.left

        if y.left != None:
            y.left.parent = v
            ls = y.left.size
        else:
            ls = 0
        y.parent = v.parent
        if v.parent == None:
            self.root =y
        elif v == v.parent.left:
            v.parent.left = y
        else:
            v.parent.right = y
        y.left = v
        v.parent = y
        tff = v.size
        tf = y.size
        y.size = tff
        v.size = tff - tf  + ls


    def right_rotate(self,v):
        y = v.left
        v.left = y.right
        if y.right != None:
            y.right.parent = v
            ls = y.right.size
        else:
            ls = 0
        y.parent = v.parent
        if v.parent == None:
            self.root = y
        elif v == v.parent.right:
            v.parent.right = y
        else:
            v.parent.left = y
        y.right = v
        v.parent = y
        tff = v.size
        tf = y.size
        y.size = tff
        v.size = tff - tf  + ls



    def rebalance(self,v):
        while (v.parent.color == "RED"):
            if v.parent == v.parent.parent.left:
                y = v.parent.parent.right
                if y != None and y.color == "RED":
                    v.parent.color = "BLACK"
                    y.color = "BLACK"
                    v.parent.parent.color = "RED"
                    v = v.parent.parent
                else:
                    if v == v.parent.right:
                        v = v.parent
                        self.left_rotate(v)
                    v.parent.color = "BLACK"
                    v.parent.parent.color = "RED"
                    self.right_rotate(v.parent.parent)
            else:
                y = v.parent.parent.left
                if y != None and y.color == "RED":
                    v.parent.color = "BLACK"
                    y.color = "BLACK"
                    v.parent.parent.color = "RED"
                    v = v.parent.parent
                else:
                    if v == v.parent.left:
                        v = v.parent
                        self.right_rotate(v)
                    v.parent.color = "BLACK"
                    v.parent.parent.color = "RED"
                    self.left_rotate(v.parent.parent)
            if(v.parent == None):
                break
        self.root.color = "BLACK"

    def insert(self,v):
        if self.root == None:
            self.root = v
            self.root.color = "BLACK"
        else:
            x = self.root
            y = None
            while x != None:
                x.size += 1
                y = x
                if v.value < x.value:
                    x = x.left
                else:
                    x = x.right

            v.parent = y
            if v.value < y.value :
                y.left = v
            else:
                y.right = v
            v.right = None
            v.left = None
            v.color = "RED"
            self.rebalance(v)



    def count_less_than(self,val):
        x = self.root
        ans = 0
        if(x == None):
            return 0
        while True:
            #print(x.value)
            if(x.right == None):
                rs = 0
            else:
                rs = x.right.size

            if(x.value < val):
                ans += x.size -rs
                x = x.right            
            elif x.value > val:
                x = x.left
            else:
                ans += x.size - rs
                return ans
            #print(ans)
            if x == None:
                return ans
#############################################################################################################################


f = open("input.txt","r")
inp = f.read()
inp = inp[0:len(inp)-2] #contains the encoding of newick tree, assuming input ends with ;

#every comma in input represents an input node and two consecutive commas always have an edge with parent being 
#the one with lower c value [number of unmatched '(' before it]

pos = dict() #we maintain this to map index of comma in input to 0...t-1 as they appear in input, where t is the number of commas in input i.e internal nodes
				#for example for ((a,b),c) {pos[3] = 0, pos[6] = 1}
c = 0
ind = 0 #to assign index of commas to numbers from 0...t
root = 0 #root of the tree, pos[i] such that index i such that inp[i] = ',' for which c = 1
t = 0 #number of internal nodes

for i in range(0, len(inp)):
	if(inp[i] == ","):
		t += 1
		if c == 1:
			root = ind
		pos[i] = ind
		ind += 1
	if(inp[i] == "("):
		c += 1
	if inp[i] == ")":
		c -= 1

#extracting words cooresponding to leafs from the input
words = []
last = -1 #to store index of last '(' or ')' or ',' hence inp[last+1:i] is the current word
for i in range(len(inp)):
	c = inp[i]
	if(c == ")" or c == "(" or c == ","):
		if last != i-1:
			words.append(inp[last+1:i])
		last = i

words.sort() #sorts the words lexicographically

wordstonum = dict() #we assign number to words starting with t in lexicographical order to make our lives easier, 0...t-1 are internal nodes and rest are leaves

it = t
for w in words:
	wordstonum[w] = it
	it += 1

adj = [[-1,-1] for x in range(t)] #adj list for binary tree
lvl = [[] for x in range(t+2)] #level of internal vertices 
depth = 0

#assigning left children to their parents

w = ""
lastComma = -1
last = -1
for i in range(len(inp)):
	c = inp[i]
	if c == "(":
		depth += 1
	if c == ")":
		depth -= 1

	if c == ",":
		lvl[depth].append(pos[i])
		if len(lvl[depth+1]) != 0: #this means there is a left child of pos[i] (pos[j] such that j < i and inp[j] = ','), we add that to adj of node pos[i]
			adj[pos[i]][0] = lvl[depth+1].pop()  #we remove it from lvl[depth+1] as it is assigned to pos[i]

	if(c == ")" or c == "(" or c == ","):
		w = inp[last+1:i]
		if c == ",":
			if w != "": 
				adj[pos[i]][0] = wordstonum[w] #this means the current word is assigned to the comma right after it
			lastComma = i
		last = i
#assigning right children to their parents in a similar way

w = ""
last = -1
depth = 0
lvvl = [[] for x in range(t+2)]

for i in range(len(inp)-1,-1,-1):
	c = inp[i]
	if c == ")":
		depth += 1
	if c == "(":
		depth -= 1

	if c == ",":
		lvvl[depth].append(pos[i])
		if len(lvvl[depth+1]) != 0:
			adj[pos[i]][1] = lvvl[depth+1].pop()
			
	if(c == ")" or c == "(" or c == ","):
		w = inp[i+1:last]
		if c == ",":
			if w != "": 
				adj[pos[i]][1] = wordstonum[w]
			lastComma = i
		last = i

#######################################################################################################################################
#newick tree made in O(n) time where n is length of input; adj is the adjency array for internal nodes


#now we do dp
#dp[v] + dp[leftchild] + dp[rightchild] + min (cr(leftchild, rightchild), cr(rightchild,leftchild))


dp = [0 for x in range(len(words) + t)]
leavesUnder = [[] for x in range(len(words) + t)]

def countCross(v): 
	if v >= t: #v is a leaf
		tree = RedBlackTree()
		tree.insert(Node(v))
		leavesUnder[v].append(v)
		return tree 
	else:
		leftChild = adj[v][0]
		rightChild = adj[v][1]

		lefttree = countCross(leftChild)
		rightree = countCross(rightChild)	

		dp[v] = dp[leftChild] + dp[rightChild] #+ minimal crossings among left child and right child whcih we calculate below

		if len(leavesUnder[leftChild]) <= len(leavesUnder[rightChild]): #left child is smaller (i.e it has less leaves under it) 
			su = 0
			for x in leavesUnder[leftChild]:
				su += rightree.count_less_than(x) #searching in RBTREE, takes log n time for each query

			ssu = len(leavesUnder[leftChild])*len(leavesUnder[rightChild]) - su  #su is the number of crossing when left child is on left
			#ssu is the numebr of crossing when right child is on left
			if(ssu < su): #we swap
				temp = adj[v][0]
				adj[v][0] = adj[v][1]
				adj[v][1] = temp
				dp[v] += ssu
			else:
				dp[v] += su

			for x in leavesUnder[leftChild]:
				rightree.insert(Node(x))		#whenever a leaf is inserted into a bigger set, the size of smaller set is doubled
				leavesUnder[rightChild].append(x) #so we can only perform this operation log n times (just like disjoint structure union)
			leavesUnder[v] = leavesUnder[rightChild] #this makes overall complexity O(nlog^2n) with O(nlogn) space 
			return rightree

		else: #right child is smaller this follows similarly to the above case
			su = 0
			for x in leavesUnder[rightChild]:
				su += lefttree.count_less_than(x)

			ssu = len(leavesUnder[leftChild])*len(leavesUnder[rightChild]) - su 

			if(su < ssu): #we swap
				temp = adj[v][0]
				adj[v][0] = adj[v][1]
				adj[v][1] = temp
				dp[v] += su 
			else:
				dp[v] += ssu
			for x in leavesUnder[rightChild]:
				lefttree.insert(Node(x))
				leavesUnder[leftChild].append(x)
			leavesUnder[v] = leavesUnder[leftChild] 
			return lefttree

countCross(root)


def makeNewick(root): #retrieving the encoding by a simple recursive fuction
	if root >= t:
		return words[root-t]
	else:
		return "(" +makeNewick(adj[root][0])+","+ makeNewick(adj[root][1]) + ")"

o = open("output.txt","w")
o.write("Best ordering: \n" + makeNewick(root) + "\nNumber of crossings: ")
o.write(str(dp[root]))





