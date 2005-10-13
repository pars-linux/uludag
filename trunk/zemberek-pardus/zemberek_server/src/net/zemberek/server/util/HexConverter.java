package net.zemberek.server.util;

import java.nio.ByteBuffer;
import java.util.StringTokenizer;

//import org.apache.commons.logging.Log;
//import org.apache.commons.logging.LogFactory;

/**
 * ��inde hex say�lar olan bir stringi byte dizisine d�n��t�r�r. Veya byte
 * dizisini i�inde hex say�lar olan stringe d�n��t�r�r
 */

public class HexConverter {
    
   //public static Log log = LogFactory.getLog(HexConverter.class);
   
   /** Hex karakterler */
   public final static char hexChars[] = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};

   /** Bu tablo da Hex karakterlerin rakamsal kar��l���n� tutar */
   public final static byte hexValTable[] = {-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
   		                                     -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
   		                                     -1,-1,-1,-1,-1,-1,0,1,2,3,4,5,6,7,8,9,-1,-1,-1,-1,-1,-1,-1,10,
   		                                     11,12,13,14,15,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
   		                                     -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,10,11,12,13,14,15,-1,-1,-1,-1,-1,
   		                                     -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
   		                                     -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
   		                                     -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
   		                                     -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
   		                                     -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
   		                                     -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
   		                                     -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1};

   /** Bu dizideki elemalar "indis" de�erlerinin Hex string kar��l���n� tutar */
   public final static String byteVal[] = {"00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
                                           "0A", "0B", "0C", "0D", "0E", "0F", "10", "11", "12", "13",
                                           "14", "15", "16", "17", "18", "19", "1A", "1B", "1C", "1D",
                                           "1E", "1F", "20", "21", "22", "23", "24", "25", "26", "27",
                                           "28", "29", "2A", "2B", "2C", "2D", "2E", "2F", "30", "31",
                                           "32", "33", "34", "35", "36", "37", "38", "39", "3A", "3B",
                                           "3C", "3D", "3E", "3F", "40", "41", "42", "43", "44", "45",
                                           "46", "47", "48", "49", "4A", "4B", "4C", "4D", "4E", "4F",
                                           "50", "51", "52", "53", "54", "55", "56", "57", "58", "59",
                                           "5A", "5B", "5C", "5D", "5E", "5F", "60", "61", "62", "63",
                                           "64", "65", "66", "67", "68", "69", "6A", "6B", "6C", "6D",
                                           "6E", "6F", "70", "71", "72", "73", "74", "75", "76", "77",
                                           "78", "79", "7A", "7B", "7C", "7D", "7E", "7F", "80", "81",
                                           "82", "83", "84", "85", "86", "87", "88", "89", "8A", "8B",
                                           "8C", "8D", "8E", "8F", "90", "91", "92", "93", "94", "95",
                                           "96", "97", "98", "99", "9A", "9B", "9C", "9D", "9E", "9F",
                                           "A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9",
                                           "AA", "AB", "AC", "AD", "AE", "AF", "B0", "B1", "B2", "B3",
                                           "B4", "B5", "B6", "B7", "B8", "B9", "BA", "BB", "BC", "BD",
                                           "BE", "BF", "C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7",
                                           "C8", "C9", "CA", "CB", "CC", "CD", "CE", "CF", "D0", "D1",
                                           "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "DA", "DB",
                                           "DC", "DD", "DE", "DF", "E0", "E1", "E2", "E3", "E4", "E5",
                                           "E6", "E7", "E8", "E9", "EA", "EB", "EC", "ED", "EE", "EF",
                                           "F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9",
                                           "FA", "FB", "FC", "FD", "FE", "FF" };
    /** prettyprint i�in parametre */ 
    public static int PRINT_ASCII_VALUES = 0;

    /**
     * Bir byte dizisini hex say�lar string'ine d�n��t�r�r. Stringde default olarak bo�luk yoktur
     * @param array Hex string'e d�n��t�r�lecek giri� dizisi
     * @return : Hexadecimal String
     */
    public static String byteArrayToHexString(byte array[]) {
		if (array == null) return "null";
		if (array.length == 0) return "empty array";
		byte strBuffer[]= new byte[array.length * 2];
		int j= 0;
		try {
			for (int i= 0; i < array.length; i++) {
				strBuffer[j++]= (byte) hexChars[(array[i] & 0xF0) >> 4];
				strBuffer[j++]= (byte) hexChars[(array[i] & 0x0F)];
			}
		}
		catch(RuntimeException e){
			//log.error("byte dizisi Hex String'e d�n��t�r�lemedi",e);
			return "";
		}
		return new String(strBuffer);
	}

    /**
     * Bir byte dizisini hex say�lar string'ine d�n��t�r�r.
     * Her hex digit aras�na default olarak bo�luk karakteri koyar
     *
     * @param array Hex string'e d�n��t�r�lecek giri� dizisi
     * @param spacer : hex de�erler aras�na konacak ay�ra� karakteri �zel olarak belirlenmek isterse buraya girilmelidir.
     * @return : Hexadecimal String
     */
    public static String byteArrayToHexString(byte array[], String spacer) {
		if (array == null) return "null";
		if (array.length == 0) return "empty array";
        int spacerLen = 0;
        if (spacer != null) spacerLen = spacer.length();
        StringBuffer str = new StringBuffer(array.length * (2+spacerLen) + 1);
        for (int i = 0; i < array.length; i++) {
        	str.append(byteVal[array[i] & 0xFF]);
        	if(spacer != null) str.append(spacer);
        }
        if(spacer!= null) str.setLength(str.length() - spacerLen);
        return str.toString();
    }

    public static String hexDump(byte array[]) {
        return byteArrayToPrettyHexString(array, PRINT_ASCII_VALUES, 16);
    }
    
    /**
     * Pretty Print As Hex. Ofset ve ascii de�erlerini de basar ve istenilen aral�klarla sat�rlara b�ler
     * @param array : Giri� disizi
     * @param type  : �imdilik ihmal ediliyor (�e�itli default t�rler olacak)
     * @param bytesPerColumn : 80 lik bir text ekranda g�r�lebilmesi i�in 16 verin, daha b�y�kler i�in 25 olabilir.
     *                         isterseniz kafan�za g�re de tak�labilirsiniz.
     * @return ��k string :)
     */
	public static String byteArrayToPrettyHexString(byte array[], int type, int bytesPerColumn) {
		if(array == null) return "Array is null.";
		if (array.length == 0) return "empty array";
		int spacerLen = 0;
		String spacer = " ";
		boolean showAscii = true;
		boolean showByteCount = true;
		// Ba�ta yaz�lan index bilgisinin uzunlu�u ne olacak?
		int lengthDigitCount = calculateDigitCount(array.length);

		if (bytesPerColumn < 1) bytesPerColumn = 1;
		if (spacer != null) spacerLen = spacer.length();

		// uygun uzunlukta bufferimizi olu�tural�m
		StringBuffer str = new StringBuffer(array.length * (4 + spacerLen) + (array.length/bytesPerColumn)*(lengthDigitCount+4) );

		// ka� segment olaca��n� hesaplayal�m
		int segments = array.length / bytesPerColumn ;

		if(array.length % bytesPerColumn != 0) segments++; // e�er sonda fazlal�k kal�rsa o da bir segment edecek

		// Giri� bilgisini yazal�m.
		str.append("\nDizi Boyu: " + array.length +"\n" );
		// Her sat�r i�in gerekli i�lemi tekrarlayaca��z
		// Bu dizi indeksi
		int index = 0;
		int expectedLen = bytesPerColumn*2+(bytesPerColumn*spacer.length());

		// Her segment i�in
		for(int i=0; i<segments; i++){
			// ka��nc� byte'den ba�l�yoruz onu yazal�m.
			if(showByteCount == true){
				str.append(padSpace(""+index,lengthDigitCount)+ ": ");
			}
			int startIndex = index;
			int strLen = 0;

			for(int j=0; j<bytesPerColumn && index<array.length; j++){
				// Hex de�erimizi ve spacer'i ekleyelim.
				str.append(byteVal[array[index++] & 0xFF]);
				if(spacer != null) str.append(spacer);
                strLen += spacer.length() + 2 ; //her byte i�in 2+spacerlen karakter
			}
			String pad = getSpacesForPadding(strLen, expectedLen);
			str.append(pad);
			str.append(" ");
			if(type == PRINT_ASCII_VALUES )
				for(int k=startIndex; k<index; k++){
	 				   str.append(getAsciiRep(array[k]));
				}
			str.append("\n");
		}
		return str.toString().trim();
	}
    /**
     * Verilen say�n�n stringhalinde ka� dijit buluaca��n� hesaplar (log10 len) asl�nda.
     * @param len
     * @return
     */
	private static int calculateDigitCount(int len){
		if(len <0) return 0;
		if(len <10) return 1;
		if(len <100) return 2;
		if(len <1000) return 3;
		if(len <10000) return 4;
		if(len <100000) return 5;
		if(len <1000000) return 6;
		return 7;
	}
   
	/**
	 * Verilen String'in boyu len olana dek sa�dan bo�luk ekler
	 * @param str
	 * @param len
	 * @return bo�luk padlenmi� string
	 */
	private static String padSpace(String str, int len){
		int padCount = len - str.length();
		if(padCount <=0 ) return str;
		for(int i=0; i<padCount; i++) str+=" ";
		return str;
	}
    /**
     * Bu da len-strlen uzunlukta bo�luklarla doldurulmu� bir String d�nd�r�r. Pretty print i�in maymun olduk.
     * @param strLen
     * @param len
     * @return
     */
	private static String getSpacesForPadding(int strLen, int len){
		int padCount = len - strLen;
		if(padCount <=0 ) return "";
		String str="";
		for(int i=0; i<padCount; i++) str+=" ";
		return str;
	}
    
	/**
	 * verilen byte de�erinin ASCII kar��l���n� String olarak d�nd�r�r. byteVal>126 i�in "." d�ner.
	 * @param byteVal
	 * @return
	 */
    public static String getAsciiRep(byte byteVal){
    	int val  = (byteVal & 0xFF);
    	String str;
    	if(val > 126 || val<' ') str = ".";
    	else str = "" + (char)val;
    	return str;
    }

    /**
     * ��inde hex say�lar olan bir string'i byte dizisine d�n��t�r�r. Default olarak Stringin i�inde rakamlar
     * aras�nda bo�luk olmad���n� kabul eder.
     * @param str : Giri� Hex stringi
     * @return : byte[] cinsinden, hex stringinin i�indeki  say�sal de�erler
     * @throws NumberFormatException
     */
    public static byte[] hexStringToByteArray(String str) throws NumberFormatException{
		if(str == null) return null;
		if(str.length() == 0) return null;
		str.trim();
		int len = str.length();
		int j=0, k=0;
		byte[] strBuf = str.getBytes();
		byte[] buf = new byte[len/2];
		if ((str.length() % 2) != 0){
		   //log.error("Bo�luksuz Hex Stringler'in boyu mutlaka �ift olmal�d�r");
		   throw new NumberFormatException("Hex String uzunlu�u �ift olmal�. String: " + str  + " Boy :" + str.length());
		}
		try {
			for (int i= 0; i < len; i += 2) {
				byte firstNibble= hexValTable[strBuf[k++]];
				byte secondNibble= hexValTable[strBuf[k++]];
				if(firstNibble == -1 || secondNibble== -1){
					//log.error("String Illegal Hex karakter ta��yor.");
					throw new NumberFormatException("String Illegal Hex karakter ta��yor. String: " + str );
				}
				buf[j++]= (byte) (firstNibble * 16 + secondNibble);
			}
		} catch (RuntimeException e) {
			//log.error("Hex String byte dizisine donusturulemedi!" + str, e);
			throw new NumberFormatException("Hatal� hex string. String: " + str );

		}
		return buf;
    }

    /**
     * ��inde hex say�lar olan bir string'i byte dizisine d�n��t�r�r. spacer Stringindeki karakterleri ay�ra� kabul eder.
     * @param str : Giri� Hex stringi
     * @param spacer : hex de�erler aras�ndaki ay�ra� karakteri �zel olarak belirlenmek isterse buraya girilmelidir.
     *                 null veya "" ise biti�ik Stringler i�in �al��r (ancak bu i� i�in tek parametreli versiyon kullan�lmal�)
     * @return : byte[] cinsinden, hex stringinin i�indeki  say�sal de�erler
     * @throws NumberFormatException
     */
    public static byte[] hexStringToByteArray(String str, String spacer) throws NumberFormatException{
        int count = 0;
        byte array[];
		if(str == null) return null;
		if(str.length() == 0) return null;
		str.trim();
		try {
			if (spacer == null || spacer.equals("")){
				if ( (str.length() % 2) != 0) {
					str = "0" + str;
				}
				array= new byte[str.length() / 2];
				for (int i= 0; i < str.length(); i += 2){
					String temp= str.substring(i, i + 2);
					array[count++]= (byte) Integer.parseInt(temp, 16);
				}
			} else {
				StringTokenizer token= new StringTokenizer(str, " ,");
				count= token.countTokens();
				array= new byte[count];
				for (int i= 0; i < count; i++){
					array[i]= (byte) Integer.parseInt(token.nextToken(), 16);
				}
			}
		} catch (RuntimeException e){
			//log.error("Hex String byte dizisine donusturulemedi!" + str, e);
			throw new NumberFormatException("Hatal� Hex String: "+ str);
		}
        return array;
    }


    // ---------- Di�er Primitif D�n���mler ----------------------------
    /**
     * Verilen bir long say�y� Hex String'e d�n��t�r�r. (Big Endian)
     * @param input hex string'e d�n��t�r�lecek long cinsinden giri�.
     * @return long giri�in Hex String kar��l���
     */
    public static String longToHexString(long input) {
        ByteBuffer buf = ByteBuffer.allocate(8); // Long de�er 8 byte
        buf.putLong(0, input);
        buf.flip();
        return byteArrayToHexString(buf.array(), null);
    }

    public static String shortToHexString(short input) {
		ByteBuffer buf = ByteBuffer.allocate(2); // Long de�er 8 byte
		buf.putShort(0, input);
		buf.flip();
		return byteArrayToHexString(buf.array(), null);
	}

	public static String byteToHexString(byte input) {
		return byteVal[input & 0xFF];
	}

	/**
     * Verilen bir Hex String'in long say� de�erini d�nd�r�r.
     * @param inputStr: Hex String
     * @return : Hex String'in long kar��l���.
     */
    public static long hexStringToLong(String inputStr) {
        byte[] tempbuff = hexStringToByteArray(inputStr, null);
        ByteBuffer buf = ByteBuffer.allocate(tempbuff.length);
        buf.put(tempbuff);
        buf.flip();
        return buf.getLong();
    }

    /**
     * Verilen bir int say�y� Hex String'e d�n��t�r�r.
     * @param input hex string'e d�n��t�r�lecek int cinsinden giri�.
     * @return int giri�in Hex String kar��l���
     */
    public static String intToHexString(int input) {
        ByteBuffer buf = ByteBuffer.allocate(4); //int de�er 4 byte
        buf.putInt(0, input);
        buf.flip();
        return byteArrayToHexString(buf.array(), null);
    }

    /**
     * Verilen bir Hex String'in int say� de�erini d�nd�r�r.
     * @param inputStr: Hex String
     * @return : Hex String'in int kar��l���.
     */
    public static int hexStringToInt(String inputStr) {
        byte[] tempbuff = hexStringToByteArray(inputStr, null);
        ByteBuffer buf = ByteBuffer.allocate(tempbuff.length);
        buf.put(tempbuff);
        buf.flip();
        return buf.getInt();
    }

    /**
     * Verilen bir Hex String'in byte say� de�erini d�nd�r�r.
     * @param inputStr: Hex String
     * @return : Hex String'in int kar��l���.
     */
    public static byte hexStringToByte(String inputStr) {
        byte[] tempbuff = hexStringToByteArray(inputStr, null);
        return tempbuff[0];
    }

}