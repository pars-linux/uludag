{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<script language="JavaScript" src="jscript/popcalendar.js"></script>
<br>
<table border=0 cellpadding="5" width="100%">
<TR>
<td>
<FIELDSET style="display:block; position:relative; top:0; width=100%">
<LEGEND>HABER EKLE</LEGEND>
<table border=0 cellpadding="0" cellspacing="0" width="80%">
	<form name="HaberDuzenle" method="POST" action="{{$Burasi}}">
	 <tr>
     <td><br>&nbsp;&nbsp;Ba�l�k</td>
	  <TD colspan="2"><br><INPUT type="text" name="YeniHaberBaslik" size="25" maxlength="255" value="{{$HaberBaslik}}">
	  </TD>
    </tr>
    <tr>
     <tr>
      <td><br>&nbsp;&nbsp;Haber Tarihi</td>
      <td>
	  	<br><input type="text" name="YeniHaberTarih" size="20" value="{{$YeniHaberTarih}}">&nbsp;
	    <input type="image" src="resimler/ew_calendar.gif" alt="Tarih Se�iniz..." onClick="popUpCalendar(this, this.form.YeniHaberTarih,'dd.mm.yyyy');return false;"></TD>
   	  </td>
    </tr>
       <td align="right" colspan="4"><br><hr><INPUT type="submit" name="Ekle" value="Ekle" accesskey="D"></td>
    </tr>
	</form>
</table>
<br>
Not: Eklemi� oldu�unuz haberin i�eri�ini, haber g�ncelle sayfas�ndan olu�turabilirsiniz.
</fieldset>
</td>
<TD valign="top" align="center">
<FIELDSET style="width=100%">
<LEGEND>HABER ARA</LEGEND>
  <table border=0 width="100%">
   <form method="POST" action="{{$Burasi}}" onsubmit="return kontrol(this)">
	<tr><td>Ba�l�k</td><td><input size=30 type="text" name="Baslik" alt="Haber Ba�l���"></td></tr>
    <tr>
      <td>Haber Tarihi</td>
      <td>
	  	<input type="text" name="Tarih" size="20" value="{{$BugunTarihi}}">&nbsp;
	    <input type="image" src="resimler/ew_calendar.gif" alt="Tarih Se�iniz..." onClick="popUpCalendar(this, this.form.Tarih,'dd.mm.yyyy');return false;"></TD>
   	  </td>
    </tr>
    <tr><td>Haber Durum</td>
    <td><select name="Durum">
	  			<option value="">Durum Se�iniz...</option>
	  			<option value="Aktif">Aktif</option>
	  			<option value="Pasif">Pasif</option>
	  			
	</select></td></tr>
	 <tr><td>Man�et Durum</td>
    <td><select name="MansetDurum">
	  			<option value="">Durum Se�iniz...</option>
	  			<option value="Aktif">Aktif</option>
	  			<option value="Pasif">Pasif</option>
	  			
	</select></td></tr>
    <tr><td colspan="3" align=right><hr><input type="submit" name="HaberAra" value="G�nder"></td></tr>
		<input type="hidden" name="HaberNo" value="{{$HaberNo}}">
   </form>
  </table>
  <!--<a href="javascript:OzelPencere('{{$ASSayfa}}HaberEkle','Onizleme',800,700,0,1)">
 Yeni Ekle</a>-->
</FIELDSET>
</TD>
<!--<TD valign="top">
{{include file=NesneDuzenle.tpl}}
</TD>-->

</TR>
<TR><TD colspan="2">
<br>
<table border=0 width=100% cellpadding=3>
{{if $Haberler}}
 <tr class=tabbas1>
 	<td>Man�et Haber</td>
 	<td>Ba�l�k</td>
 	<td>Tarih</td>
 	<td>Durum</td>
 	<td>��lem</td>
 </tr>
 {{foreach item=Haber from=$Haberler name=Haber}}
  {{if $smarty.foreach.Haber.iteration is odd}}<tr class=tabloliste1>{{else}}<tr class=tabloliste2>{{/if}}
     <td><a href="{{$Burasi}}&HaberNo={{$Haber.No}}&Manset={{if $Haber.Manset eq 'Aktif'}}Pasif{{else}}Aktif{{/if}}" title="Haberi Man�et Yapmak i�in T�klay�n�z!">{{$Haber.Manset}}</a></td>
     <td>{{$Haber.Baslik}}</td>
     <td>{{$Haber.Tarih}}</td>
    <!-- <td width="509">{{$Haber.Icerik}}</td>
     <td><img src="../templates/resimler/extras/{{$Haber.Resim}}" width="50" height="50"></td>-->
    <td><a href="{{$Burasi}}&HaberNo={{$Haber.No}}&Aktif={{if $Haber.Durum eq 'Aktif'}}Pasif{{else}}Aktif{{/if}}" title="Haberi Aktif veya Pasif Yapmak i�in T�klay�n�z!">{{$Haber.Durum}}</a></td>
     <td align=center>
         <a href="javascript:OzelPencere('{{$ASSayfa}}HaberDuzenle&HaberNo={{$Haber.No}}','Onizleme',450,200,0,1)">
        <img src="{{$WebAdminResimler}}/duzenle.gif" border=0 alt="D�zenle"></a><br><hr>
        <a onclick="return confirm('{{$Haber.Baslik}} Haber haberi silmek istedi�inize emin misiniz?')"
        href="{{$Burasi}}&Sil={{$Haber.No}}"><img src="{{$WebAdminResimler}}/sil.gif" border=0 alt="Sil"></a>
     </td>
   </tr>
 {{/foreach}}
{{else}}
 <tr><td align=center><b>Kay�tl� Haber bulunmamaktad�r.</b></td></tr>
{{/if}}
</table>
</td></TR></table>
{{/strip}}