{{strip}}
{{include file="ModulTop.tpl" bgcolor="$sistem_Modul_HaberArama"}}
<table border="0" cellspacing="0" cellpadding="1" width="100%">
  <tr>
  <form action="{{$SSayfa}}Arama" method="post">
  <TD valign=middle>
  <table border=0 align="center"><TR><TD><strong>{{t}}Site i�i Arama{{/t}}</strong></TD></tr>
  <tr>
        <td>
        <input type="text" size="15" name="Aranacak" value="Site i�i Arama"  maxlength=49 onfocus="if ( value == 'Site i�i Arama' ) { value = ''; }" onblur="if ( value == '' ) { value = 'Site i�i Arama'; }" >
        </td>
        <td align="right"><input class="button" name="ara" type="submit" value="  {{t}}Ara{{/t}}  "></td>
  </tr>
  <tr>
        <td align="center" colspan="2"><a href="{{$SSayfa}}Arama">{{t}}Detayl� Arama{{/t}}</a></td>
  </tr>
  </form>
  </table>
 </td>
 </tr>
</table>
{{include file="ModulFoot.tpl"}}
{{/strip}}