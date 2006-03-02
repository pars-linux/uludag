<?
// require_once($INI_OrtakDosyalarDizin.'/Fonksiyonlar/ileti.php');
require_once("$KutuphaneDizin/Pear/Mail.php");
require_once("$KutuphaneDizin/Pear/Mail/mimePart.php");
require_once("$KutuphaneDizin/Pear/Mail/mime.php");

class Ileti
{
var $Ayarlar=array();
var $IletiIcerik;
var $IcerikTamam = false;
var $BaslikTamam = false;
var $Baslik;
var $Gonderen;

var $Iletici;
var $Mime;

function IcerikYeni($Icerik,$Tur = 'Html')	// Verilen icerigi ileti icerigine yazar. Tur 'Html' veya 'Duzyazi' olabilir
	{
	if($Tur != 'Duzyazi')
		{
		$this->Ayarlar["content_type"]="text/html";
		$this->Ayarlar["charset"]="iso-8859-9";
	        $this->Ayarlar["encoding"]="7bit";
		$this->IletiIcerik = $Icerik;
		}
	else
		{
		$this->Ayarlar["content_type"]="multipart/alternative";
		$this->Ayarlar["encoding"]="7bit";
		$this->Ayarlar["charset"]="iso-8859-9";
		$this->IletiIcerik = $Icerik;
		}
	$this->IcerikTamam = true;
	}

function IcerikHazir($IcerikDosya,$Degiskenler,$Tur = 'Html')	// Verilen dosya ismini IletiDosyalar tablosunda bulup, icerik alir
	// Tur: Sistem Degiskenleri kismindan belirlenir, eger belirlenmemisse Html Varsayilan olarak secilir... Degistirmenize gerek yoktur.
	{
	global $SmartyIletiIcerik;
	$Sorgu1 = sorgula("SELECT Dosya FROM IletiDosyalar WHERE Isim='$IcerikDosya'");

	if(list($vt_Dosya) = $Sorgu1->fetchRow())
		{
		if($Tur != 'Duzyazi')
			{
			$this->Ayarlar["content_type"]="text/html";
			$this->Ayarlar["charset"]="iso-8859-9";
			$this->Ayarlar["encoding"]="7bit";
			ob_start();
                        if ($Degiskenler)
                        {
                foreach($Degiskenler as $Isim => $Deger)
				$SmartyIletiIcerik->assign($Isim,$Deger);
                        }
			
                        include($SmartyIletiIcerik->template_dir."/ust_html.tpl");
			$SmartyIletiIcerik->display("html_$vt_Dosya.tpl");
			include($SmartyIletiIcerik->template_dir."/alt_html.tpl");
			$this->IletiIcerik = ob_get_contents();
			ob_end_clean();
			}
		else
			{
			$this->Ayarlar["content_type"]="multipart/alternative";
			$this->Ayarlar["encoding"]="7bit";
			$this->Ayarlar["charset"]="iso-8859-9";
			ob_start();
			include($SmartyIletiIcerik->template_dir."/ust_yazi.tpl");
			include($SmartyIletiIcerik->template_dir."/$vt_Dosya.tpl");
			include($SmartyIletiIcerik->template_dir."/alt_yazi.tpl");
			$this->IletiIcerik = ob_get_contents();
			ob_end_clean();
			}
		$this->IcerikTamam = true;
		}
	else	$this->IcerikTamam = false;
	}

function Baslik($Baslik)
	{
	$this->Baslik = $Baslik;
	if($Baslik)	$this->BaslikTamam = true;
	}

function Gonderen($EPosta)
	{
	  $this->Gonderen = $EPosta;
	}

function Gonder($Kime,$Dosya='')
	{
        
        if ($Dosya<>"")
        {
         $crlf = "\r\n";
         $hdrs = array(
              'MIME-Version' => '1.0', 
              'From'    => $this->Gonderen,
              'Subject' => $this->Baslik,
              );

        $mime = new Mail_mime($crlf);
        $mime->setHTMLBody($this->IletiIcerik);
        $mime->addAttachment($Dosya);

        $body = $mime->get();
        $hdrs = $mime->headers($hdrs);

        $mail =& Mail::factory('mail');
        $mail->send($Kime, $hdrs, $body);
        }
        else
        {
        
	if(!$this->IcerikTamam)
		return 'IcerikHazirDegil';
	else if(!$this->BaslikTamam)
		return 'BaslikHazirDegil';
        
	$this->Mime=new Mail_mimePart($this->IletiIcerik,$this->Ayarlar);
	$this->Iletici = & Mail::factory("mail");
    $Icerik=$this->Mime->encode();
	$Icerik["headers"]["MIME-Version"]="1.0";
	$Icerik["headers"]["Subject"]=$this->Baslik;
	$Icerik["headers"]["From"]=$this->Gonderen;
	if (!$this->Iletici->send($Kime,$Icerik["headers"],$Icerik["body"]) ) 
          return false;
        else
          return true;

       }
    }
}
?>
