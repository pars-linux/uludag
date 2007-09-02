""" Modules that signs and verifies pkcs 7 documents"""
from M2Crypto import BIO, Rand, SMIME, X509
from M2Crypto import m2
from cUtil import Cutil

from x5Util import X509Man


class pkcs7Work(object):
    """ Just a simple try"""
    
    def __init__(self):
        self.sm=SMIME.SMIME()
        
        
    
    def signer(self):
        """ Try to sign it """
        
    def makebuf(self,txt):
        """ Makes a text buffer"""
        return BIO.MemoryBuffer(txt)
    
    def make_sign(self,keyplace,certplace,txt,signature_place):
        """ We give the cert and key place"""
        
        #create a buffer to store the data to be signed
        tosign=self.makebuf(txt)
        
        
        
        self.p7=self.sm.load_key(keyplace,certplace)
        
        flagset=SMIME.PKCS7_DETACHED
        
        print "The flagset is :",flagset
        
        self.p7=self.sm.sign(tosign,flags=flagset)
        
        
        """SMIME.PKCS7_DATA
        SMIME.PKCS7_DETACHED
        SMIME.PKCS7_ENVELOPED
        SMIME.PKCS7_NOATTR
        SMIME.PKCS7_NOCERTS
        SMIME.PKCS7_NOCHAIN
        SMIME.PKCS7_NOINTERN
        SMIME.PKCS7_NOSIGS
        SMIME.PKCS7_NOVERIFY
        SMIME.PKCS7_SIGNED
        SMIME.PKCS7_SIGNED_ENVELOPED
        SMIME.PKCS7_TEXT
        """
        """print type(self.sm)
        print "Detached",m2.PKCS7_DETACHED
        print "Signed And Enveloped",m2.PKCS7_SIGNED_ENVELOPED
        print "Signed Only",m2.PKCS7_SIGNED
        print "No Verify",m2.PKCS7_NOVERIFY
        print "No sigs",m2.PKCS7_NOSIGS
        print "No Chain",m2.PKCS7_NOCHAIN
        print "No intern",m2.PKCS7_NOINTERN
        print "Binary",m2.PKCS7_BINARY
        print "Data",m2.PKCS7_DATA
        print "Enveloped",m2.PKCS7_ENVELOPED
        print "No attr",m2.PKCS7_NOATTR
        """
        #print  self.p7
        
        out=BIO.MemoryBuffer()
        self.p7.write(out)
        
        #res=-1
        #print out.read()
        
        #Storing the signature into a file
        
        res=Cutil.file_operator(signature_place, 1, out.read())
        
        if res and res!=-1:
            print "The signature saved to :%s"%(signature_place)
        else:
            print "Writing to file failed"
        #print self.p7.type()
        
    
    def verify_sign(self,data,signature_place):
        """ Verifies the signature against the data"""
        self.dataBuf=self.makebuf(data)
        
        
        #print self.dataBuf.read()
        
        self.p7=SMIME.load_pkcs7(signature_place)
        print "The p7 file loaded"
        
        
        #xStack=X509.X509_Stack()
        x509 = X509.load_cert('sert/newcert.pem')
        sk = X509.X509_Stack()
        sk.push(x509)
        self.sm.set_x509_stack(sk)
        
        xStore=X509.X509_Store()
        xStore.load_info("sert/newcert.pem")
        self.sm.set_x509_store(xStore)
    
        #flagset=SMIME.PKCS7_DETACHED | SMIME.PKCS7_SIGNED
        
        #xStack= self.p7.get0_signers(xStack)
        
        
        
        #xStore.add_x509(xStack.pop())
        
        #xMan=X509Man(xStack.pop())
        #self.sm.set_x509_store()
        
        
        #print xMan.list_info()
        
        flagset=SMIME.PKCS7_NOVERIFY
        print self.sm.verify(self.p7,self.dataBuf,flags=flagset)
        

if __name__=="__main__":
    
    pkc=pkcs7Work()
    #pkc.make_sign("sert/newkey.pem", "sert/newcert.pem", "Selmlar","signature.sig")
    pkc.verify_sign("Selmlare", "signature.sig")