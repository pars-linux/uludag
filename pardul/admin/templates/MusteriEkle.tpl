{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<script language="JavaScript" src="jscript/popcalendar.js"></script>
<script language="JavaScript" type="text/javascript">
function AcUlke () {
 	var SehirSec = document.UyeKayit.Vilayet;
 	var UlkeSec = document.UyeKayit.Ulke;
	secim = UlkeSec.options[UlkeSec.selectedIndex].value;
	if (secim == 'Türkiye') {
		SehirSec.disabled = false;
		
	}
	else
	{
		SehirSec.disabled = true;
		SehirSec.selectedIndex = 0;
	}

}
</script>
<script language="JavaScript" type="text/javascript">
function AcOzellik () {
 	var TescilNo = document.UyeKayit.TescilNumarasi;
 	var Ciro = document.UyeKayit.Ciro;
 	var EANTip = document.UyeKayit.EANTip;
 	var MMNMDurum = document.UyeKayit.MMNMDurum;
	secim = MMNMDurum.options[MMNMDurum.selectedIndex].value;
	if (secim == 'Evet') {
		TescilNo.disabled = false;
		Ciro.disabled=true;
		EANTip.disabled=true;
		EANTip.selectedIndex = 0;
		Ciro.selectedIndex = 0;
	}
	else
	{
		if (secim == 'Hayir' ){
		TescilNo.disabled = true;
		Ciro.disabled=false;
		EANTip.disabled=false;
		}else{
		TescilNo.disabled = true;
		Ciro.disabled=true;
		EANTip.disabled=true;
		}
		
	}

}
</script>
<script language="JavaScript" src="jscript/popcalendar.js"></script>

<table width="100%" border=0 align=center cellpadding="4" cellspacing="1" style="border-collapse:collapse ">
   <form name="UyeKayit" action="{{$Burasi}}" method=post onsubmit="if (SifreKontrol()) return kontrol(this); else return false;">
     <tr class=tabbas1><td height=33 colspan=2>MÜÞTERÝ EKLEME</td></tr>
      <tr bgcolor="#f4f4f4">
        <td width="150"><font color="#FF0000">*</font><b>Yetkili Ad Soyad</b></td>
        <td bgcolor="#f4f4f4"><input name="N_AdSoyad" type="text" value="" alt="Ad Soyad" size=30></td>
      </tr>
      <tr>
        <td width="150"><font color="#FF0000">*</font><b>Firma Unvan</b></td>
        <td><input name="N_FirmaUnvan" type="text" value="" alt="Firma Ünvan" size=30></td>
      </tr>
       <tr bgcolor="#f4f4f4">
        <td width="150"><font color="#FF0000">*</font><b>Firma Kýsa Ad</b></td>
        <td bgcolor="#f4f4f4"><input name="N_FirmaAd" type="text" value="" alt="Firma Ad" size=30></td>
      </tr>
      <tr>
       <td width="150"><font color="#FF0000">*</font><b>E-Posta Adresi</td>
       <td><input name="N_EPosta1" type="text" value="" alt="Kullanýcý Ad" size=30>&nbsp;
        Kullanýcý adý olarak kullanýlacaktýr.
       </td>
     </tr>
      <tr bgcolor="#f4f4f4">
       <td width="150"><font color="#FF0000">*</font><b>Þifre</td>
       <td bgcolor="#f4f4f4"><input name="N_Sifre" type="password" value=""  alt="Þifre">&nbsp;
         Þifreniz en az 6 hane olmalýdýr.</td>
     </tr>
       <tr>
       <td width="150"><font color="#FF0000">*</font><b>Þifre Tekrarý</td>
       <td><input name="N_SifreTekrar" type="password" value=""  alt="Tekrar Þifre"></td>
     </tr>
      <tr bgcolor="#f4f4f4">
        <td width="150"><font color="#FF0000">*</font><b>Telefon Numarasý</b></td>
        <td bgcolor="#f4f4f4"><input name="N_Tel" type="text" onkeypress="HarfYok();" value="" alt="Telefon Numarasý" size=30></td>
      </tr>
      <tr>
        <td width="150"><b>Fax Numarasý</b></td>
        <td ><input name="Fax" type="text" value="" alt="Fax Numarasý" size=30 onkeypress="HarfYok();"></td>
      </tr>
      <tr bgcolor="#f4f4f4">
       <td width="150"><font color="#FF0000">*</font><b>Adres</td>
       <td><TEXTAREA name="N_Adres" alt="Adres" cols="30" rows="2" ALT="Adres"></TEXTAREA></td>
     </tr>
     
      <tr>
       <td><font color="#FF0000">*</font><b>Ýl</b></td>
       <td>
       <select name="N_Vilayet" alt="Ýl">
          {{html_options options=$Vilayetler}}
        </select>    
         Eðer Ülke alanýndan Türkiye'yi seçerseniz Vilayet seçebilirsiniz.
         </td>
        </tr>
       <tr   bgcolor="#f4f4f4">
        <td width="150"><b>Web Adresi</b></td>
        <td ><input name="URL" type="text" value="http://" alt="Web Adresi" size=30></td>
      </tr>
       <tr>
        <td width="150"><b>Vergi Dairesi</b></td>
        <td bgcolor="#f4f4f4"><input name="VergiDaire" type="text" alt="Vergi Dairesi" size=30></td>
      </tr>
      <tr   bgcolor="#f4f4f4">
        <td width="150"><b>Vergi Numarasý</b></td>
        <td ><input name="VergiNo" type="text" alt="Vergi Numarasý" size=30 onkeypress="HarfYok();"></td>
      </tr>
      <tr>
      		<td>
      			<font color="#FF0000">*</font><b>Daha Önce Milli Mal Numaralama Merkezi'ne üye olup Firmanýz adýna Barkod Numarasý Aldýnýz mý?</b>
      		</td>
      		<td>
      			<select name="MMNMDurum">
      				<option value="">Lütfen Seçiniz...
      				<option value="Evet">Evet
      				<option value="Hayir">Hayýr
      			</select>&nbsp;&nbsp;&nbsp;	
      		<input name="TescilNumarasi" onkeypress="HarfYok();" type="text" alt="Tescil Numarasý" size=20 value="Tescil Numarasý..." onfocus="if ( value == 'Tescil Numarasý...' ) { value = ''; }" onblur="if ( value == '' ) { value = 'Tescil Numarasý...'; }" maxlength="15">	
      		</td>
      </tr>
       <tr bgcolor="#f4f4f4">
      	<td>
      		<font color="#FF0000">*</font><b>Firmanýz Adýna Milli Mal Numaralandýrma Merkezine Baþvurunuz Bizim Tarafýmýzdan Yapýlsýn mý?</b>
      	</td>
      	<td>
      		<select name="MMNMBasvuru">
      				<option value="">Lütfen Seçiniz...
      				<option value="Evet">Evet
      				<option value="Hayir">Hayýr
      			</select>
      	</td>
      </tr>
       <tr bgcolor="#f4f4f4">
        <td width="150"><b>Ciro/YTL</b></td>
        <td >
          <select name="Ciro">
          	<option value="">Lütfen Seçiniz...
        	<option value="A">100 Milyon ve üzeri
        	<option value="B">50-100 Milyon arasý
        	<option value="C">10-50 Milyon Arasý
        	<option value="D">1-10 Milyon Arasý
        	<option value="E">500 Bin- 1 Milyon Arasý
        	<option value="F">100-500 Bin  Arasý
        	<option value="G">25-100 Bin Arasý
        	<option value="H">0-25 Bin Arasý ve YENÝ KURULANLAR
        	
         </select>
        </td>
      </tr>       
       
       <tr>
        <td width="150"><b>EAN.UCC Firma Numarasý</b></td>
        <td>
        <select name="EANTip" >
        	<option value="">Lütfen Seçiniz...
        	<option value="9">9 Basamaklý
        	<option value="8">8 Basamaklý
        	<option value="7">7 Basamaklý
        </select><br>
        	<table border="0">
        		<tr bgcolor="#FFFFFF">
        			<td>
        				* Ürün çeþitlerimin sayýsý <b>1000</b>'i aþmadýðýndan <b>9 basamaklý</b> EAN.UCC firma numarasý tahsis edilmesi uygundur.
        			</td>
        		</tr>
        		<tr>
        			<td>
        				* Ürün çeþitlerimin sayýsý <b>1000</b>'i aþtýðýndan 10.000 çeþit ürünümü numaralandýrmaya olanak tanýyan <b>8 basamaklý</b> EAN.UCC firma numarasý tahsis edilmesi uygundur.  
        			</td>
        		</tr>
        		<tr bgcolor="#FFFFFF">
        			<td>
        				* Ürün çeþitlerimin sayýsý <b>10.000</b>'i aþtýðýndan 100.000 çeþit ürünümü numaralandýrmaya olanak tanýyan <b>7 basamaklý</b> EAN.UCC firma numarasý tahsis edilmesi uygundur.  
        			</td>
        		</tr>
        	</table>
        </td>
      </tr>	
	   <tr>
        <td width="150" bgcolor="#f4f4f4"><font color="#FF0000">*</font><b>Ürün Sayýsý</b></td>
        <td bgcolor="#f4f4f4"><input name="N_UrunCesit" onkeypress="HarfYok();" type="text" alt="Ürün Çeþit" size=30> Firmanýza ait ürün çeþiti sayýsý. </td>
      </tr>	

      <tr>
       <td width="150">
        Haber listesinde üyelik ister misiniz?        Sitemizdeki yenilikler ve yeni ürünler adresinize gönderilecektir. </td>
       <td>
        <input name="HaberListe" type=checkbox value="Evet" checked id="HaberUyelik">
        <label for="HaberUyelik">Evet üye olmak istiyorum.</label> </td>
     </tr>
      <tr bgcolor="#f4f4f4">
   <td class=tdbaslik>MMNM Vekalet</td>
   <td><input type="checkbox" name="MMNMVekalet" {{if $Uye.MMNMVekalet}} checked {{/if}}></td>
 	</tr>
 	<tr>
   <td class=tdbaslik>TOF Belge</td>
   <td><input type="checkbox" name="TOFBelge" {{if $Uye.TOFBelge}} checked {{/if}}></td>
 </tr>
 <tr bgcolor="#f4f4f4">
   <td class=tdbaslik>Özel Vekalet</td>
   <td><input type="checkbox" name="OzelVekalet" {{if $Uye.OzelVekalet}} checked {{/if}}></td>
 </tr>
 	<tr>
   <td class=tdbaslik>Gelir Tablosu</td>
   <td><input type="checkbox" name="GelirTablosu" {{if $Uye.GelirTablosu}} checked {{/if}}></td>
 </tr>  
 <tr bgcolor="#f4f4f4">
   <td class=tdbaslik>Sicil Gazete</td>
   <td><input type="checkbox" name="SicilGazete" {{if $Uye.SicilGazete}} checked {{/if}}></td>
 </TR>
   
      <tr>
    <td colspan=10 align=right>
        <input name="UyeKayit" type="submit" value="K a y d e t" class="onay">   
        
        </td>
     </tr>
     
  </form>
</table>
   <br>

<SCRIPT language="javascript">
 function SifreKontrol()
  {
    var sifre=document.UyeKayit.N_Sifre.value;
    if((sifre.length<6)&&(sifre!=''))
    {
       alert('Þifreniz en az 6 haneli olmalýdýr!');
       return false;
    }

    if(document.UyeKayit.N_Sifre.value != document.UyeKayit.N_SifreTekrar.value)
     {
      alert("Þifreleriniz Uyuþmamakta!");
      return false;
     }
     else return true;
  }

</SCRIPT>

{{/strip}}