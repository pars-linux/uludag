from sign.cert import X509Man
from htmlTemplate import certInfo 
#temp
from initializer import DbCert
#system import
import os
#3rd party
from M2Crypto import X509 as x

class ListDb(X509Man):
    """ that class wll generate some info about the certs and chains in a readable format"""
    
    def __init__(self,buffer=None,filer=None):
        """ initialize thing to show can be a buffer or a file..."""
        #the html that will be stored
        self.certText=""
        
        #initializing the cert there is nothing now
        #test=open("test.cert","w")
        #test.write(buffer)
        #test.close()
        
        #cert=x.load_cert("test.cert")
        
        super(ListDb,self).__init__()
        
        if buffer:
            super(ListDb,self).set_from_buf(buffer)
            print 
            #print super(ListDb,self).check_sum()
            #print super(ListDb,self).get_detail()
            
        
        
        
    def per_info(self):
        """ Generates the part that is concerned with issuer and subject"""
        issuer=super(ListDb,self).get_detail("issuer")
        subject=super(ListDb,self).get_detail("subject")
        dater=super(ListDb,self).get_date_info()
        
        self.cert="".join([certInfo['beginTag'],certInfo['personData']%("Issuer Info",issuer['country'],issuer['commoName'],\
                        issuer['eadress'],issuer['statePro'],issuer['department'],issuer['company']),certInfo['personData']\
                        %("Subject Info",subject['country'],subject['commoName'],\
                        subject['eadress'],subject['statePro'],subject['department'],subject['company']),\
                        certInfo['dateInfo']%(dater['v'],dater['sdate'],dater['edate']),certInfo['endTag']])
        
        tofile=open("test.html","w")
        tofile.write(self.cert)
        tofile.close()
        
        os.system("/usr/bin/firefox test.html")
        
        
        
        
        
if __name__=="__main__":
    dc=DbCert()
    
    
    l=ListDb(buffer=dc.get_certData(7)[1:])
    l.per_info()