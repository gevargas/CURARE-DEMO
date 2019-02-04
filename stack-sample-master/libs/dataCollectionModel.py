
# coding: utf-8

# # Data Collection Model

# ## Data Collection Class

# In[1]:


class DataCollection:
    _id = ""
    name = ""
    provider = ""
    licence = ""
    size = 0
    author = ""
    description = ""        
    
    releaseList = []
 
    def __init__(self, _id, name, provider, licence, size, author, description, releaseList):
        self._id = _id
        self.name = name
        self.provider = provider
        self.licence = licence
        self.size = size
        self.author = author
        self.description = description
        
        self.releaseList = releaseList
 
    def printInfo(self):
        print ("_id  = " + str(self._id))
        print ("name  = " + str(self.name))
        print ("provider  = " + str(self.provider))
        print ("licence  = " + str(self.licence))
        print ("size = " + str(self.size) + " Bytes")
        print ("author  = " + str(self.author))
        print ("description  = " + str(self.description))
        print ("list of releases = " + str(self.releaseList))      
        
print ("DataCollection class created!")


# ## Release Class

# In[2]:


class Release:
    _id = ""
    releaseNum = 0
    publicationDate = ""    
    
    itemList = []
    size = 0   # added by me
    
    def __init__(self, _id, releaseNum, publicationDate, itemList, size):
        self._id = _id
        self.releaseNum = releaseNum
        self.publicationDate = publicationDate        
        self.itemList = itemList
        self.size = size
        
    def incRelease(self):
        self.releaseNum = self.releaseNum + 1    
        
    def printInfo(self):
        print ("_id  = " + str(self._id))
        print ("releaseNum  = " + str(self.releaseNum))
        print ("publicationDate  = " + str(self.publicationDate))                
        print ("List of items = " + str(self.itemList))
        print ("size = " + str(self.size) + " Bytes")

print ("Release class created!")


# ## Item Class

# In[3]:


class Item:
    _id = ""
    name = ""
    content = []
    
    size = 0   # added by me
 
    def __init__(self, _id, name, content, size):
        self._id = _id
        self.name = name
        self.content = content
        self.size = size
        
    def printInfo(self):
        print ("_id  = " + str(self._id))
        print ("name  = " + str(self.name))
        print ("content  = " + str(self.content))
        print ("size = " + str(self.size) + " Bytes")

print ("Item class created!")

