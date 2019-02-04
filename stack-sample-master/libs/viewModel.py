
# coding: utf-8

# # View Model 

# ## View class

# In[2]:


class View:
    _id = "" # url
    name = ""
    provider = ""
    author = ""
    description = ""        
    releaseViewList = []
 
    def __init__(self, _id, name, provider, author, description, releaseViewList):
        self._id = _id
        self.name = name
        self.provider = provider
        self.author = author
        self.description = description
        self.releaseViewList = releaseViewList
 
    def printInfo(self):
        print ("_id = " + str(self._id))
        print ("name = " + str(self.name))
        print ("provider = " + str(self.provider))
        print ("author = " + str(self.author))
        print ("description = " + str(self.description))
        print ("list of release views = " + str(self.releaseViewList))    
        
print ("View class created!")


# ## Release View class

# In[3]:


class ReleaseView:
    _id = "" # url
    version = 0
    publicationDate = ""
    size = 0
    licence = ""                
 
    def __init__(self, _id, version, publicationDate, size, license, attributeDescList):
        self._id = _id
        self.version = version
        self.publicationDate = publicationDate
        self.size = size
        self.license = license        
        self.attributeDescList = attributeDescList        
 
    def printInfo(self):
        print ("_id  = " + str(self._id))
        print ("name  = " + str(self.name))
        print ("provider  = " + str(self.provider))
        print ("author  = " + str(self.author))
        print ("description  = " + str(self.description))
        print ("default  = " + str(self.default))
        print ("list of release views = " + str(self.releaseViewList)) 
        
print ("ReleaseView class created!")


# ## Attribute Descriptor class

# In[4]:


# One instance per item
class AttributeDescriptor:
    _id = "" # should be the same as the one in data collection model. Created by mongo
    name = "" # name of the item
    _type = [] # maybe take from data collection model
    valueDistribution = [] # Histogram
    nullValue = 0               
    absentValue = 0 
    minValue = []
    maxValue = []
    mean = []
    median = []
    mode = []
    count = 0
 
    def __init__(self, _id, name, _type, valueDistribution, nullValue, absentValue, minValue, maxValue, mean, median, mode, count):
        self._id = _id
        self.name = name
        self._type = _type
        self.valueDistribution = valueDistribution
        self.nullValue = nullValue
        self.absentValue = absentValue
        self.minValue = minValue
        self.maxValue = maxValue
        self.mean = mean
        self.median = median
        self.mode = mode
        self.count = count
 
    def printInfo(self):
        print ("_id = " + str(self._id))
        print ("name = " + str(self.name))
        print ("_type = " + str(self._type))
        #print ("valueDistribution = " + str(self.valueDistribution))
        print ("nullValue = " + str(self.nullValue))
        print ("absentValue = " + str(self.absentValue))
        print ("minValue = " + str(self.minValue))
        print ("maxValue = " + str(self.maxValue))
        print ("mean = " + str(self.mean))
        print ("median = " + str(self.median))
        print ("mode = " + str(self.mode)) 
        print ("count = " + str(self.count)) 
        
print ("AttributeDescriptor class created!")

