/*
 * Created on 17.Ara.2004
 *
 */
package net.zemberek.server;

/**
 * @author MDA & ER
 *
 */
public interface ZemberekSessionListener {

    public void zemberekSessionReady(ZemberekSession session);
    public void messageReceived(ZemberekSession session, ZemberekMesaji mesaj);
}
