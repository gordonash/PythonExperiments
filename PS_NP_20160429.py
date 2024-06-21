# ProfStatusCheckFromFile2.py

import dnuk_config as config
import time
import sys

from bs4 import BeautifulSoup
from urllib import urlopen
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence
from sqlalchemy.sql import text as SQLQuery
from sqlalchemy.schema import Index
from datetime import datetime   

app = Flask(__name__)

CurrentConfig = config.DevelopmentConfig
app.config['SQLALCHEMY_DATABASE_URI'] = CurrentConfig.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = CurrentConfig.SQLALCHEMY_COMMIT_ON_TEARDOWN
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CurrentConfig.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['IMPRESSION_LOGGING_ON'] = CurrentConfig.IMPRESSION_LOGGING_ON
app.config['DEBUG'] = CurrentConfig.DEBUG
app.config['WTF_CSRF_ENABLED'] = CurrentConfig.WTF_CSRF_ENABLED
app.config['SECRET_KEY'] = CurrentConfig.SECRET_KEY

db = SQLAlchemy(app)

def GetURL(providerid):
    # first lookup the URL to be used for this providerid
    searchurl = ""
    thisProvider = ProfessionalStatusProvider.query.filter_by(providerid=providerid).first()
    if thisProvider.providerid == providerid:
        providername = thisProvider.providername
        searchurl = thisProvider.searchurl
    if verbose==True: TimePrint(providername,'','')
    if verbose==True: TimePrint(searchurl,'','')
    return searchurl
    
def RunTestOne(providerid):
    # use the next to test for one that does exist
    GMC="7041223" 
    # use the next to test for one that does NOT exist
    #GMC="0123456"
    GMC="6106364"
    searchurl = GetURL(providerid)
    keyvalue = GMC
    timestamp = CheckProviderPerson(providerid,searchurl,keyvalue)
    return 1

def RunTestBatch(providerid):
    searchurl = GetURL(providerid)
    keyvalue = "7041223" 
    timestamp = CheckProviderPerson(providerid,searchurl,keyvalue)
    keyvalue = "0123456"
    timestamp = CheckProviderPerson(providerid,searchurl,keyvalue)
    keyvalue = "6160746"
    timestamp = CheckProviderPerson(providerid,searchurl,keyvalue)
    keyvalue = "6053958"
    timestamp = CheckProviderPerson(providerid,searchurl,keyvalue)
    return 4
    
def RunQueryList(providerid):
    # get the list of GMC numbers that need checking
    rows = 0
    searchurl = GetURL(providerid)
    querystring = 'EXEC ProfessionalStatus_WorkList_sp ' + str(providerid)
    sql = SQLQuery(querystring)
    result = db.engine.execute(sql)
    names = []
    for name in result:
        keyvalue = name
        names.append(keyvalue)
        #TimePrint(keyvalue,'','')
        timestamp = CheckProviderPerson(providerid,searchurl,keyvalue)
        rows = rows + 1        
    return rows
    
def RunFileList(providerid,filename):
    rows = 0
    searchurl = GetURL(providerid)
    with open(filename) as f:
        lines = f.read().splitlines()
        for line in lines:
            keyvalue = line
            #print keyvalue
            timestamp = CheckProviderPerson(providerid,searchurl,keyvalue)
            rows = rows + 1        
    return rows

def CheckProviderPerson(providerid,searchurl,keyvalue):
    GivenName = ""
    Surname = ""
    membertype = ""
    category = ""
    Country = ""
    GMCRef = ""   
    response = ""
    try:
        link = searchurl + keyvalue
        doc = urlopen(link).read()
        # get the content
        soup = BeautifulSoup(doc, 'html.parser')

        if providerid == 1: 
            # NHS provider
            # find the table
            table = soup.find('table', {'class': 'listing sortable'})
            #TimePrint(table,'','') 
            rows = table.find_all('tr')
            # the second row has the date we seek
            row = rows[1] # zero-based array
            # get the <td> as a list of cells
            cells = row.find_all('td')
            # six <td>
            membertype = cells[0].find(text=True)
            membertype = membertype.strip()
            GMCRef = cells[1].find(text=True)
            GMCRef = GMCRef.strip()
            Fullname = cells[2].find(text=True)
            Fullname = Fullname.strip()
            GivenName = ""
            Surname = ""
            response = cells[3].find(text=True)
            response = response.strip()
            category = cells[4].find(text=True)
            category = category.strip()

        elif providerid == 2:
            # RCGP
            #print(soup)
            table = soup.find('table', {'class': 'membersearch-results full'})
            rows = table.find_all('tr')
            # the second row has the date we seek
            row = rows[1] # zero-based array
            # get the <td> as a list of cells
            cells = row.find_all('td')
            # six <td>
            GivenName = cells[0].find(text=True)
            GivenName = GivenName.strip()
            Surname = cells[1].find(text=True)
            Surname = Surname.strip()
            membertype = cells[2].find(text=True)
            membertype = membertype.strip()
            category = cells[3].find(text=True)
            category = category.strip()
            Country = cells[4].find(text=True)
            Country = Country.strip()
            response = cells[5].find(text=True)
            response = response.strip()

        else:
            membertype = "Not a performer"
    except:
        membertype = "Not found"
    
    if response is None: response = ""
    logdate = datetime.now().isoformat()
    if verbose==True: TimePrint(keyvalue,membertype,'')

    # does this person already exist?
    thisPerson = ProfessionalStatusPerson.query.filter_by(providerid=providerid,keyvalue=keyvalue).first()
    if thisPerson is None:
        logdate = CreatePersonRecord(providerid, keyvalue, membertype, category, response)
    else:
        thisPerson.logdate = logdate
        thisPerson.membertype = membertype
        thisPerson.category = category
        thisPerson.response = response
        db.session.commit()

    #TimePrint("waiting 2 seconds..."
    time.sleep(2)

    return logdate

class ProfessionalStatusProvider(db.Model):
    __tablename__ = 'professional_status_provider'
    providerid = db.Column(db.Integer, primary_key=True)
    providername = db.Column(db.String(100))
    searchurl  = db.Column(db.String(100))
    keyname  = db.Column(db.String(20))
    lastchecked = db.Column(db.DateTime)
    lastkeyvalue = db.Column(db.String(100))
    
    def __init__(self, providerid, providername, searchurl, keyname, lastchecked, lastkeyvalue):
        self.providerid = providerid
        self.providername = providername
        self.searchurl = searchurl
        self.keyname = keyname
        self.lastchecked = lastchecked
        self.lastkeyvalue = lastkeyvalue

    def __repr__(self):
       return "<ProfessionalStatusProvider(providerid='%s',providername='%s', searchurl='%s', keyname='%s', lastchecked='%s', lastkeyvalue='%s')>" % (
       self.providerid, self.providername, self.searchurl, self.keyname, self.lastchecked, self.lastkeyvalue)    


professional_status_person_pid_seq = Sequence('professional_status_person_pid_seq')           
class ProfessionalStatusPerson(db.Model):
    __tablename__ = 'professional_status_person'
    pid = db.Column(db.Integer, professional_status_person_pid_seq, 
             server_default=professional_status_person_pid_seq.next_value(), primary_key=True)
    providerid = db.Column(db.Integer)
    keyvalue = db.Column(db.String(20))
    logdate = db.Column(db.DateTime)
    membertype = db.Column(db.String(50))
    category = db.Column(db.String(50))
    response = db.Column(db.String(1000)
    )
    	
    def __init__(self, pid, providerid, keyvalue, logdate, membertype, category, response):
        self.id = pid
        self.providerid = providerid
        self.keyvalue = keyvalue
        self.logdate = logdate
        self.membertype = membertype
        self.category = category
        self.response = response

    def __repr__(self):
       return "<ProfessionalStatusPerson(pid='%s',providerid='%s',keyvalue='%s', logdate='%s', membertype='%s', category='%s', response='%s')>" % (
       self.pid, self.providerid, self.keyvalue, self.logdate, self.membertype, self.category, self.response)
       
def CreatePersonRecord(providerid, keyvalue, membertype, category, response):
    logdate = datetime.now().isoformat()
    thisPerson = ProfessionalStatusPerson(None, providerid, keyvalue, logdate, membertype, category, response)
    db.session.add(thisPerson)
    db.session.commit()
    pid = thisPerson.pid
    return pid  

def TimePrint(item1,item2,item3):
    logdate = datetime.now().isoformat()
    #python2
    if sys.version_info[0] < 3:
        if len(item1)>0 and len(item2)>0 and len(item3)>0:
            print logdate,':',item1,':',item2,':',item3
        if len(item1)>0 and len(item2)>0 and len(item3)==0:
            print logdate,':',item1,':',item2
        if len(item1)>0 and len(item2)==0 and len(item3)==0:
            print logdate,':',item1
    #python3
    if sys.version_info[0] == 3:
        if len(item1)>0 and len(item2)>0 and len(item3)>0:
            print (logdate,':',item1,':',item2,':',item3)
        if len(item1)>0 and len(item2)>0 and len(item3)==0:
            print (logdate,':',item1,':',item2)
        if len(item1)>0 and len(item2)==0 and len(item3)==0:
            print (logdate,':',item1)
    return 

#-----------------------------------------------------------------------------------------------------------------
# start here
#-----------------------------------------------------------------------------------------------------------------

#datafile = './Data/GMC_test10.txt'
datafile = './Data/GMC_NP_20160422.txt'
verbose = True
# -- set the providerid to be checked
providerid = 1 # NHS Performer
#providerid = 2 # RCGP
rows_processed = 0

if verbose==True: TimePrint('--------------------------------------------------------','','')
if verbose==True: TimePrint('Started','','')
if verbose==True: TimePrint('Data file',datafile,'')

#rows_processed = RunTestOne(providerid)
#rows_processed = RunTestBatch(providerid)
#rows_processed = RunQueryList(providerid)
#rows_processed = RunFileList(providerid,datafile)

if verbose==True: TimePrint('rows_processed = '+str(rows_processed),'','')
if verbose==True: TimePrint('Finished!','','')
if verbose==True: TimePrint('--------------------------------------------------------','','')

#-----------------------------------------------------------------------------------------------------------------

