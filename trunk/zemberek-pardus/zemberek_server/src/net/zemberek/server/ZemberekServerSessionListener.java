/*
 * @(#) $Id: ZemberekServerSessionListener.java,v 1.5 2005/08/26 17:40:52 mdakin Exp $
 */
package net.zemberek.server;

import java.util.HashMap;

import net.gleamynode.netty2.Message;
import net.gleamynode.netty2.Session;
import net.gleamynode.netty2.SessionListener;

/**
 * {@link SessionListener}for SumUp server.
 * 
 * @author Trustin Lee (http://gleamynode.net/)
 * @version $Rev: 49 $, $Date: 2005/08/26 17:40:52 $
 */
public class ZemberekServerSessionListener implements SessionListener{

    //private static final Log log = LogFactory.getLog(ZemberekServerSessionListener.class);
    Server myServer = null;
    HashMap sessionList = new HashMap();

    public ZemberekServerSessionListener(Server server) {
        myServer = server;
    }

    public void connectionEstablished(Session session) {
        if(session.getSocketAddressString().indexOf("127.0.0.1") == -1){
            System.out.println("Zemberek sunucusu sadece yerel soket üzerinden hizmet verir. " + session.getSocketAddressString());
            session.close();
            return;
        }
        ZemberekSession zemberekSession = new ZemberekSession(session);
        zemberekSession.setDinleyici(myServer);
        sessionList.put(session, zemberekSession);
        System.out.println("Connection Established.");
    }

    public void connectionClosed(Session session) {
        //SessionLog.info(log, session, "Connection closed.");
        sessionList.remove(session);
    }

    public void messageReceived(Session session, Message message) {

        ZemberekSession zemberekSession = (ZemberekSession) sessionList.get(session);
        if (zemberekSession == null) {
            System.out.println("Session listede bulunamadı");
            return;
        }
        zemberekSession.messageReceived(session, message);
        //SessionLog.info(log, session, "RCVD: " + message);
    }

    public void messageSent(Session session, Message message) {

        ZemberekSession zemberekSession = (ZemberekSession) sessionList.get(session);
        if (zemberekSession == null) {
            System.out.println("Session listede bulunamadı");
            return;
        }
        zemberekSession.messageSent(session, message);
        //SessionLog.info(log, session, "SENT: " + message);
    }

    public void sessionIdle(Session session) {
        ZemberekSession zemberekSession = (ZemberekSession) sessionList.get(session);
        if (zemberekSession == null) {
            System.out.println("Session listede bulunamadı");
            return;
        }
        zemberekSession.sessionIdle(session);
        //SessionLog.warn(log, session, "Disconnecting the idle.");
        session.close();
    }

    public void exceptionCaught(Session session, Throwable cause) {
        ZemberekSession zemberekSession = (ZemberekSession) sessionList.get(session);
        if (zemberekSession == null) {
            //log.debug("Session listede bulunamadı");
            return;
        }
        zemberekSession.exceptionCaught(session,cause);
 
        //SessionLog.error(log, session, "Unexpected exception.", cause);
        // close the connection on exceptional situation
        session.close();
    }
}