{{strip}}
{{include file="Stil.tpl"}}
<body onload="document.GirisFormu.username.focus()" bgcolor="#d9dddf">
<title>Yönetim Konsolu Giriþi</title>
<br>
{{if $UyariIleti}}<center><b>{{$UyariIleti}}</center>{{/if}}
<br><br>
 <table align=center cellpadding=5 border=0>
 <tr class=tabbas1><td colspan=2><b>YÖNETÝCÝ GÝRÝÞÝ</b></td></tr>	
 <form name="GirisFormu" method="post" action="">
  <tr>
   <td>
	  <table border=0 cellpadding=10>
            <tr>
           		<td class=kalinsag>Kullanýcý Adý:</td>
            	<td><input type="text" name="username"></td>
           </tr>
	   	   <tr>
	    		<td class=kalinsag>Þifre:</td>
	    		<td><input type="password" name="password"></td>
	   	   </tr>
	   	   <tr>
	     		<td colspan=2 align=right><input type="submit" name="Gir" value="Giriþ" class="onay"></td>
	   	   </tr>
	  </table>
   </td>
 </tr>
 </form>
 </table>
 <table align=center>
	<tr>
		<td align=center>
		by R. Tolga KORKUNCKAYA (2005) tolga@forsnet.com.tr
		</td>
	</tr>
 </table>
{{/strip}}
