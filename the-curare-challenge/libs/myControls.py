
# coding: utf-8

# In[1]:


import time, threading
import ipywidgets as widgets

class myControls:
    # btn - receive a button object
    # lbl - receive a label object
    #    we use lbl.value to get timer value
    # q - receive a multiple option object
    #    we use q.value to get answered value
    def timer(btn,lbl,q):        
            
        cnt =int(lbl.value)   
        on=btn.value 
        desc=q.description

        if desc!='Submitted':
            if on==True:      
                threading.Timer(1, timer, [btn,lbl,q]).start()
                cnt = cnt+1                        
                lbl.value = str(cnt)
                btn.description='Submit answer'
                q.disabled=False

            elif on==False:
                threading.Timer(1, timer, [btn,lbl,q]).start()
                btn.description='Activate'
                q.disabled=True

            else:
                None
        
        if cnt!=0 and btn.description=='Activate':
            threading.Timer(1, timer, [btn,lbl,q]).start()
            q.description='Submitted'
            btn.visibility='hidden'
            btn.description='--'
            btn.disbled=True    

