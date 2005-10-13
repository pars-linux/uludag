/*
 * Created on 14.Ara.2004
 *
 */
package net.zemberek.client;

import java.io.IOException;
import java.net.InetSocketAddress;

import net.gleamynode.netty2.IoProcessor;
import net.gleamynode.netty2.MessageRecognizer;
import net.gleamynode.netty2.OrderedEventDispatcher;
import net.gleamynode.netty2.Session;
import net.gleamynode.netty2.ThreadPooledEventDispatcher;
import net.zemberek.server.Config;
import net.zemberek.server.TestMesaji;
import net.zemberek.server.ZemberekMesaji;
import net.zemberek.server.ZemberekMessageRecognizer;
import net.zemberek.server.ZemberekSession;
import net.zemberek.server.ZemberekSessionListener;

//import org.apache.commons.logging.Log;
//import org.apache.commons.logging.LogFactory;


/**
 * @author MDA & ER
 *
 */
public class TestClient extends Thread implements ZemberekSessionListener{
    //private static final Log log = LogFactory.getLog(TestClient.class);

    private static final String HOSTNAME = "localhost";
    private static final int CONNECT_TIMEOUT = 60; // seconds

    private static IoProcessor ioProcessor = new IoProcessor();
    private static ThreadPooledEventDispatcher eventDispatcher = new OrderedEventDispatcher();
    private Session session = null;
    private String name;
    private ZemberekSession zemberekSession = null;

    public TestClient(String name) {
        this.name = name;
    }

    public void init() {
        try {
            ioProcessor.start();
            eventDispatcher.setThreadPoolSize(2);
            eventDispatcher.start();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    public String toString() {
        return this.name;
    }

    public void connect() {
        // prepare message recognizer
        MessageRecognizer recognizer = new ZemberekMessageRecognizer();
        // create a client session
        session = new Session(ioProcessor, new InetSocketAddress(HOSTNAME, Config.serverPort), recognizer, eventDispatcher);
        // set configuration
        session.getConfig().setConnectTimeout(CONNECT_TIMEOUT);
        zemberekSession = new ZemberekSession(session);
        zemberekSession.setDinleyici(this);
        session.addSessionListener(zemberekSession);
        session.start();
    }

    public void run() {
        init();
        connect();
        System.out.println(session.getSocketAddress() + " 'a Zemberek istemcisi olarak baglaniyorum. ");
        disconnect();
    }

    public void disconnect() {
        while (!zemberekSession.isSonlandi()) {
            try {
                Thread.sleep(400);
            }
            catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        System.out.println("Disconnected! " +  name);
    }

    public static void main(String[] args) {
        TestClient client = new TestClient("Zemberek Test Client");
        client.start();
    }

    public void zemberekSessionReady(ZemberekSession session) {
        System.out.println("Zemberek Session ready. sending request");
        session.mesajYaz(new TestMesaji("* tes"));
        session.mesajYaz(new TestMesaji("& tes"));
        session.mesajYaz(new TestMesaji("& XXX"));
        session.mesajYaz(new TestMesaji("* MERHABA"));
        session.mesajYaz(new TestMesaji("* s\u00f6\u011f\u00fc\u015f"));
        session.mesajYaz(new TestMesaji("* MRHABA"));
        session.mesajYaz(new TestMesaji("& MRHABA"));
        session.mesajYaz(new TestMesaji("& LMA"));
        session.mesajYaz(new TestMesaji("23423423"));
        session.mesajYaz(new TestMesaji("* merhaba elma yesene hedehodo zemberek"));
        session.mesajYaz(new TestMesaji("23423423"));
    }

    public void messageReceived(ZemberekSession session, ZemberekMesaji mesaj) {
        System.out.println("Mesaj geldi " + mesaj);
    }


}
