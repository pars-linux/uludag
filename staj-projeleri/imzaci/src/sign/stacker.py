from M2Crypto import X509

from x5Util import X509Man


class stackWork(object):
    """ That class will handle the certification chains"""
    
    def __init__(self,nStack=None):
        """ Make a stack object"""
        if nStack:
            self.st=nStack
        else:
            self.st=X509.X509_Stack()
        
    #No usage for NOWW!
    def add_chain(self,file_list):
        """ Takes the file list of the files that should 
        construct the chain. It is better list to be in sequence from ca to client"""
        
        for x in file_list:
            cert=X509.load_cert(x)
            print self.st.push(cert)
            
        print "The chain was loaded"
            

    def print_all(self):
        """ Gets all the cert to be shown"""
        xs=self.st.pop()
        xShow=X509Man(xs)
        
        while xs:
            print "######################################################"
            xShow.list_info()
            del xShow
            xs=self.st.pop()
            xShow=X509Man(xs)
            print "######################################################"
        
            
        print "End of the show"
        
        
if __name__=="__main__":
    stack=stackWork()
    stack.create_chain(["chain/cacert.pem","chain/cert1.pem","chain/cert2.pem"])
    stack.print_all()