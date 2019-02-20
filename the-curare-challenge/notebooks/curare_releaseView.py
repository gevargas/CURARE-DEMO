import pandas as pd
import timeit
import ipywidgets as widgets
import time, threading
import json
import pymongo
from pymongo import MongoClient
import pprint
import urllib.parse
import matplotlib.pyplot as plt 


def getViewsMongo():
    client = MongoClient("mongodb://adminUser:xpass@cluster0-shard-00-00-nlbcx.mongodb.net:27017/?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    db = client.test 
    db = client['stackoverflow-dump-view']
    collection = db['viewModel-view']
    return collection

def getReleaseViewNullValues(view):
    nullsView=[]
    for i in view['attributeDescList']:
        nullsView.append(sum(i['nullValue']))
    return nullsView

def countReleaseViewItems(view):
    count=[]
    for i in view['attributeDescList']:
        count.append(i['count'])
    return count

def getReleaseViewSchemata(view, dataCollections):
    schema = []
    j = 0
    for i in view['attributeDescList']:
         y = (i['_type'])
         schema.append((dataCollections[j],y))
         j = j + 1
    return schema

def getReleaseViewschema(schema, collectionName):
    j = 0
    schema_collection = (0,0)
    
    for j in range(0,len(schema)):
        
         if    schema[j][0] == collectionName:
                    schema_collection = ((collectionName, schema[j][1]))
                    return schema_collection
                
def getSchemaAttributes(rawAttributes):
  
    i = 0
    attributes = []
    for j in range(0, len(rawAttributes[1])):
        attributes.append((rawAttributes[1][j]['py/tuple'][0], rawAttributes[1][j]['py/tuple'][1]))
           
    return (rawAttributes[0], attributes)    
                
def getReleaseViewAttributesStats(view, collectionID):
    name = view['attributeDescList'][collectionID]['name']
    count= view['attributeDescList'][collectionID]['count']
    minValue = view['attributeDescList'][collectionID]['minValue']
    maxValue = view['attributeDescList'][collectionID]['maxValue']
    meanValue= view['attributeDescList'][collectionID]['mean']
    medianValue = view['attributeDescList'][collectionID]['median']
    nullValue = view['attributeDescList'][collectionID]['nullValue']
    return (name, count, minValue, maxValue, meanValue, medianValue, nullValue)

def buildTabularReleaseViewAttributeStats(schema, collectionID, releaseViewStats, columns):
    i = 0
    stats = []
    for i in range(0, len(schema[collectionID][1])):
         stats.append((schema[collectionID][1][i]['py/tuple'][0],  releaseViewStats[2][i],  releaseViewStats[3][i],  releaseViewStats[4][i],  releaseViewStats[5][i],  releaseViewStats[6][i]))

    df = pd.DataFrame(stats)
    df.columns = columns
    return df

def plotDataFrame(df, storeFileName):
    my_colors = ['b', 'r', 'g', 'y', 'm', 'c']
    ax = df.plot(kind='barh', stacked=True, color=my_colors, figsize=(12, 6))
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(storeFileName, dpi=300, bbox_inches='tight')

def plotViewReleasesRecordsNumber(releases, attributes, yLabels, xlabel, ylabel, title):
    
    i = 0

    for i in range(0, len(releases)):
        plt.plot(attributes, releases[i], label = yLabels[i])
    
    # naming the x axis 
    plt.xlabel(xlabel) 
    # naming the y axis 
    plt.ylabel(ylabel) 
    # giving a title to my graph 
    plt.title(title) 
    # show a legend on the plot 
    plt.legend() 
    # function to show the plot 
    plt.show() 
    