function TarihGecerli(Tarih)
{
  var RegExp = /^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.((19|20)\d{2})$/
  if (Tarih=="") 
    return true;
  else
    return RegExp.test(Tarih);
}


function mailkontrol(strValue) {
var objRegExp  = /(^[a-z]([a-z_\.]*)@([a-z_\.]*)([.][a-z]{2})$)|(^[a-z]([a-z_\.]*)@([a-z_\.]*)(\.[a-z]{3})(\.[a-z]{2})*$)/i;
 return objRegExp.test(strValue);
}

function MailKontrolEt(Email)
{
  if(Email=="")
    return true;
  else
  {
   if(mailkontrol(Email)==false)
   {alert('Lütfen geçerli bir email adresi giriniz!');return false;}
     else return true;
  }
}


function goster(YetkiTanim)
{
var uyari = "butonyetkiyok";
var sol = (screen.availWidth-199)/2;
if(document.layers)
document.poppedLayer = eval('document.layers[`uyari]');
else if(document.all)
document.poppedLayer = eval('document.all[uyari]');
else if(indow.navigator.userAgent.toLowerCase().match("gecko"))
document.poppedLayer = eval('document.getElementById(uyari)');
document.poppedLayer.style.top = "200";
document.poppedLayer.style.left = sol;
document.poppedLayer.style.visibility = "visible";
document.yetkihatasigosterenform.YetkiTanim.value=YetkiTanim;
}

function sakla(gelen)
{
if(document.layers)
	document.poppedLayer = eval('document.layers[`gelen]');
else if(document.all)
	document.poppedLayer = eval('document.all[gelen]');
else if(window.navigator.userAgent.toLowerCase().match("gecko"))
	document.poppedLayer = eval('document.getElementById(gelen)');
document.poppedLayer.style.visibility = "hidden";
}

function sifrekontrol(sifre1,sifre2,formad,mesaj,karakteraz)
{
    var formadi=eval("document."+formad);
    var sifredeger1=eval(formadi.name+"."+sifre1);
    var sifredeger2=eval(formadi.name+"."+sifre2);
    if (sifredeger1.value.length<6)
    {
      alert(karakteraz);
      return false;
    }
    if (sifredeger1.value!=sifredeger2.value)
    {
      alert(mesaj);
      return false;
    }
}

function BlokSaklaGoster(gelen)
	{
	kat = document.getElementById(gelen);
        if (!kat) return true;
	if(kat.style.display=='none')
		{ kat.style.display = 'block'; }
	else
		{ kat.style.display = 'none'; }
	}

function HarfYok()
{
 if (( (event.keyCode<48)&&(event.keyCode!=46)) || (event.keyCode>57))
     event.keyCode = 0;
}


function hepsinisec(formname)
{
  var formad=eval("document."+formname);
  with (formad) {
    for (var i=0; i < elements.length; i++) {
        if (elements[i].type == 'checkbox')
           elements[i].checked = true;
    }
  }
}


function hepsinitemizle(formname)
{
  var formad=eval("document."+formname);
  with (formad) {
    for (var i=0; i < elements.length; i++) {
        if (elements[i].type == 'checkbox')
           elements[i].checked = false;
    }
  }
}

function TamEkranPencere(Adres)
{
    var TamPencere=window.open(Adres,"Pencere","toolbar=0,location=0,history=1,directories=0,status=1,menubar=0,scrollbars=1,resizable=yes");
    TamPencere.focus();
}

function KapatYenile()
{
  self.close();
  self.opener.location.reload();
}

//Acilan sayfanýn tam ekran olmasý isteniyorsa
function TamEkran()
{
  window.moveTo(0,0);
  if (document.all) {
   top.window.resizeTo(screen.availWidth,screen.availHeight);
  }
  else if (document.layers||document.getElementById)
  {
      if (top.window.outerHeight<screen.availHeight||
          top.window.outerWidth<screen.availWidth)
      {
          top.window.outerHeight = screen.availHeight;
          top.window.outerWidth = screen.availWidth;
       }
  }
}//function


function OzelPencere(Adres,Tanim,En,Boy,Scroll,YeniPencerede)
{
   var ScrollVar;
   if (Scroll==1) ScrollVar=1;else ScrollVar=0;
   if (YeniPencerede==1) Yenide='_blank';else Yenide='a';
   var Ust=(screen.availHeight-Boy)/2;
   var Sol=(screen.availWidth-En)/2;
   var OzelPencere=window.open(Adres,Yenide,"toolbar=0,location=0,history=1,directories=0,status=1,menubar=0,scrollbars="+ScrollVar+",left="+Sol+",top="+Ust+ ",width="+En+",height="+Boy+",resizable=no");
   OzelPencere.focus();
}

function kontrol(gelen)
{
var hatali=false;
var regexpI = /\b.*I_.*\b/;
var toplam = gelen.elements.length;
for(i=0;i<toplam;i++)
        {
        if(gelen.elements[i].name.substring(0,2) == 'N_' && gelen.elements[i].value=='')
                {
                alert(gelen.elements[i].alt+' boþ olamaz!');
                gelen.elements[i].focus();
                hatali = true;
                break;
                }
        else if(gelen.elements[i].name.match(regexpI) && isNaN(gelen.elements[i].value))
                {
                alert(gelen.elements[i].alt+' sayý olmalýdýr!');
                gelen.elements[i].focus();
                hatali = true;
                break;
                }
        
        if ( (gelen.elements[i].name=='EPosta') || (gelen.elements[i].name=='N_EPosta') )
        {
            sonuc = MailKontrolEt(gelen.elements[i].value);
            if (sonuc==false)
            {
              gelen.elements[i].focus();
              hatali=true;
            }
        }
        
        if (gelen.elements[i].type=="text")
        {
            var ad = gelen.elements[i].name;
            sayi = ad.indexOf('Tarih');
            if (sayi!=-1)  
            {
               sonuc = TarihGecerli(gelen.elements[i].value);
               if (sonuc==false){alert('Lütfen geçerli bir tarih giriniz! Format: GG.AA.YYYY'); gelen.elements[i].focus(); hatali=true;}          
            }
        }
      

        }
if(hatali)      return false;
else            return true;
}

function SifirlarKirmizi(gelen)
{
var toplam = gelen.elements.length;
for(i=0;i<toplam;i++)
	{
	if(gelen.elements[i].type=="" || gelen.elements[i].type=="text")
		if(gelen.elements[i].value=='0')
                {
			gelen.elements[i].style.backgroundColor='#FF0000';
			gelen.elements[i].style.color='#FFFFFF';
                }

	}
}

function basamakla(Nesne)
    {
	var regexp = /[^0-9]/g
	var a = [];
        ilkdeger = Nesne.value;
	ilkdeger = ilkdeger.replace(regexp,'');
        while(ilkdeger.length > 3)
       		{
        	sonuc = ilkdeger.substr(ilkdeger.length-3);
		a.unshift(sonuc);
		ilkdeger = ilkdeger.substr(0,ilkdeger.length-3);
        	}
	if(ilkdeger.length > 0) { a.unshift(ilkdeger); }
	ilkdeger = a.join(',');
        Nesne.value = ilkdeger;
     }
