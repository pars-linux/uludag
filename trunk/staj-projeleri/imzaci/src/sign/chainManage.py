from cUtil import Cutil
from cert import X509Man
from stacker import stackWork

from M2Crypto import X509 

class chainMan(object):
    """ Loads, creates and controls the chains"""
    
    def __init__(self):
        self.__certs=[] #Will store the certs
        self.__cert_stack=[] #The lat chain
        
    
    def load_chain(self,file_list):
        """ Gets the certs from a list of files"""
        for file in file_list:
            
            xm=X509Man(X509.load_cert(file))
            
            #We should make some main verifications first checksum of the cert we load
            if not xm.check_sum():
                return False #it was modified
            
            #chect its dates
            if not xm.is_valid():
                return False
            
            self.__certs.append([xm.person_info("issuer"),xm.person_info(),xm.get_cert()])
            del xm
            
        return True
            
        #print self.__certs
        
    def create_chain(self):
        """ From files that are uploaded by args creates a valid chain
        True if created,else False"""
        
        found=False


        for i in self.__certs:
            
            if i[0]==i[1]:
                
                #print "The root Ca is :%s"%(i[0])
                self.__cert_stack.append(self.__certs.pop(self.__certs.index(i)))
                
                find=self.__cert_stack[0][0]
                found=True
                
                break
        
        if not found: # So we should choose a starting point
            issuer_list=[i[0] for i in self.__certs]
            sub_list=[i[1] for i in self.__certs]
            
            for i in issuer_list:
                if not i in sub_list:
                    #print "The starting point is :%s"%(i)
                    found=True
                    find=i #The next issuer to search
                    
                    break # No need to stay anymore
                
        while found :
            
    
    #Before enter set it
            found=False
            
            for cert in self.__certs: 
                if find==cert[0]:
                    
                    find = cert[1]
                    found = True
                    #Remove from the list
                    self.__cert_stack.append(self.__certs.pop(self.__certs.index(cert)))
                    break #out of the loop
            
            if not self.__certs:
                found = False
        
        if self.__certs:
            #print "The chain can not be constructed "
            #print "Remaining :%s"%(self.__certs)
            del self.__cert_stack
            return False
            
        else :
            #print "The cert chain is as follow:"
            #print self.__cert_stack
            return True
   
    
    def dumpto_stack(self):
        """ That one dumps all the stuff created with create_chain method"""
        newStack=X509.X509_Stack()
        
        for i in self.__cert_stack:
            newStack.push(i[2])
            
        return newStack    

    def get_final(self):
        if self.__cert_stack:
            return self.__cert_stack
        else:
            return None
            
if __name__=="__main__":
    c=chainMan()
    c.load_chain(["chain/cacert.pem","chain/cert1.pem","chain/cert2.pem"])
    c.create_chain()
    
    #Test with the stack
    
    #st=stackWork(c.dumpto_stack())
    #st.print_all()