#from pysqlite2 import dbapi2 as sqlite
import sqlite
import base64

from dbMain import LiteDb
from queryList import dbConstants
from digest.Hasher import DigestMan
from sign.chainManage import chainMan
from sign.cert import X509Man

class DbCert(LiteDb):
    """Will import,initialize,delete,list features from db that
    certs and chains are stored"""
    
    def __init__(self):
        """ Triggers the parent one to be initialized"""
        #print sqlInitCom['dbname']
        super(DbCert,self).__init__(dbConstants.DBNAME)
        cert=X509Man()
        
    
    def c_tables(self):
        """ Creates tables and triggers needed for certificate management"""
        query=list(dbConstants.sqlInitCom.keys())
        query.sort()
        
        #print query
        
        
        for q in query:
            #print q
            res=super(DbCert,self).updateS(dbConstants.sqlInitCom[q])
        
            if res==-1:
                return False
        
        print "Initializtion done..."
        
        return 0
    
    def import_cert(self,parent_chain,cert_list):
        """ That one will import the cert into the db"""
        #q="insert into certs values (null,1,\'naberlan blob\','12345')"
        #q="update certs set ch_id=12 where ce_id=1"
        
        for c in cert_list:
            tempCert=X509Man(c[2])
            q="insert into certs values (null,%s,'\%s\',\'%s\')"%(parent_chain[0],tempCert.get_cert_text(),c[0])
            #print q
            res=super(DbCert,self).updateS(q)
            del tempCert
        
            if res==-1:
            
                print "Cert insertion Failed"
                return False
            #print "Cert inserted"
        
        return True#success 
            
    def import_chain(self,file_list):
        """ Inserts a new entry to db in chain table also calls the
        import_cert to complete the job
        1.take cert stack
        2.compute their hash
        3.if chain exists it fails
        4.if root exists warning
        5.If not there it is inserted as trusted cause we import it (May be changed later)"""
        
        """ Verification Process"""
        ch=chainMan()
        if not ch.load_chain(file_list):
            print "Cert verification failed"
            return False
        
        #Test the chain if it is valid
        if not ch.create_chain():
            print "The chain is not valid"
            return False
        
        #get the final one
        chain_st=ch.get_final()
        del ch
        
        #use the slot 0 of the list that we recieved
        
        #get the hashes
        
        for c in chain_st:
            #print c[2]
            tempCert=X509Man(c[2])
            c[0]=DigestMan.gen_buf_hash(tempCert.get_cert_text())
            del tempCert
            #print c[0]
         
        #check first if the same chain is in the db
        if not self.dup_control([c[0] for c in chain_st]):
            print "The chain exists in the db"
            return False
        
        #return "Process cut :)"
        
        q="insert into chains values (null,\'name1\',\'trusted\')"
        q2="select * from chains"
        
        res=super(DbCert,self).updateS(q)
        
        
        if res==-1:
            print "Chain insertion error"
            return False
        print "New chain inserted"
        
        #super(DbCert,self).renew_conn()
        
        res=super(DbCert,self).selectS(q2)
        
        
        if not res or res==-1:
            #print res
            print "Chain insertin process failed"
            return False
        
        print "parent chain number taken"
        
        
        if not self.import_cert(res[0], chain_st):
            return False
        
        print "Import process succesfull"
        return True
        
        
        
    def delete_chain(self,cid):
        """ Deletes a chain from th db so all certs are gone in that case"""
        q="delete from chains where c_id=1"
        
        res=super(DbCert,self).updateS(q)
        
        if res!=-1:
            print "Succes"
        else :
            print "Failed"
 
    
    def dup_control(self,hash_list):
        """ Checks if the current chain is already in the db.If there is a duplication return False
        else return True"""
        
        q1="select c_id from chains order by c_id"
        res=super(DbCert,self).selectS(q1)
        
        #print hash_list
        #If there is no chains
        if not res:
            return True
        
        for ch_id in res:
            print ch_id
            #The res is a tuple in a list if present
            res=super(DbCert,self).selectS("select cert_sum from certs where ch_id=%s order by ce_id"%(ch_id))
            
            #The control is from the root to end
            #the root control...
            if res[0][0]==hash_list[0]:
                print "Root exists"
                #here we may have a raw_input to ask to user if we want to continue
                return False
            
            #if root not equal and num of items it has are not same so it is not in db
            if len(res)!=len(hash_list):
                print "Length failure"
                return False
            
            for cert in res:
                #if the hashes are same
                if list(cert)==hash_list:
                    print "The hashes are same"
                    return False
                
                
            
        return True
        #q2="select cert_sum from certs where ch_id=? order by ce_id"
        
    
    def get_certData(self,cert_id):
        """ Pulls a cert from db to show its content ..."""
        
        q="select cert_data from certs where ce_id=%s"%(cert_id)
        
        res=super(DbCert,self).selectS(q,"one")
        #print res.encode()
        
        if not res:
            return False
        
        #should convert to a good format
        
        #return res[0][1:]
        return res[0]
        #return  base64.encodestring(res[0]) 
        
        
        

if __name__=="__main__":
    dc=DbCert()
    #print dc.c_tables()
    #dc.import_cert()
    print dc.import_chain(["chain/cert2.pem"])
    #dc.delete_chain(1)
    #"chain/cacert.pem",
    #print dc.get_certData(2)