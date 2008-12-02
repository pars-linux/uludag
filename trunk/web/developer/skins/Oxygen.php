<?php
/**
 * MonoBook nouveau
 *
 * Translated from gwicke's previous TAL template version to remove
 * dependency on PHPTAL.
 *
 * @todo document
 * @package MediaWiki
 * @subpackage Skins
 */

if( !defined( 'MEDIAWIKI' ) )
	die( -1 );

/** */
require_once('includes/SkinTemplate.php');

/**
 * Inherit main code from SkinTemplate, set the CSS and template filter.
 * @todo document
 * @package MediaWiki
 * @subpackage Skins
 */
class SkinOxygen extends SkinTemplate {
	/** Using oxygen. */
	function initPage( &$out ) {
		SkinTemplate::initPage( $out );
		$this->skinname  = 'oxygen';
		$this->stylename = 'oxygen';
		$this->template  = 'OxygenTemplate';
	}
}

/**
 * @todo document
 * @package MediaWiki
 * @subpackage Skins
 */
class OxygenTemplate extends QuickTemplate {
	/**
	 * Template filter callback for MonoBook skin.
	 * Takes an associative array of data set from a SkinTemplate-based
	 * class, and a wrapper for MediaWiki's localization database, and
	 * outputs a formatted page.
	 *
	 * @access private
	 */
	function execute() {
		// Suppress warnings to prevent notices about missing indexes in $this->data
		wfSuppressWarnings();

?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="<?php $this->text('lang') ?>" lang="<?php $this->text('lang') ?>" dir="<?php $this->text('dir') ?>">
	<head>
		<meta http-equiv="Content-Type" content="<?php $this->text('mimetype') ?>; charset=<?php $this->text('charset') ?>" />
		<?php $this->html('headlinks') ?>
		<title><?php $this->text('pagetitle') ?></title>
		<style type="text/css">
		.cp-doNotDisplay { display: none; }
		@media aural, braille, handheld, tty { .cp-doNotDisplay { display: inline; speak: normal; }}
		.cp-pagetools { text-align: right; }
		@media print, embossed { .cp-pagetools { display: none; }}
		</style>
		<link rel="stylesheet" media="screen,projection" type="text/css" title="KDE Colors" href="<?php $this->text('stylepath') ?>/oxygen/css.php?mode=normal&amp;css-inc=/" />
		<link rel="stylesheet" media="print, embossed" type="text/css" href="<?php $this->text('stylepath') ?>/oxygen/css.php?mode=print&amp;css-inc=/" />
		<!--[if IE 6]> <link rel="stylesheet" type="text/css" media="screen" title="KDE Colors - ie Fix" href="$this->text('stylepath') ?>/oxygen/ie_fix.css" />  <![endif]-->
		<link rel="alternative stylesheet" media="screen, aural, handheld, tty, braille" type="text/css" title="Flat" href="<?php $this->text('stylepath') ?>/oxygen/css.php?mode=flat&amp;css-inc=/" />
		<link rel="alternative stylesheet" media="screen" type="text/css" title="Browser Colors" href="<?php $this->text('stylepath') ?>/oxygen/css.php?color&amp;background&amp;link" />
		<link rel="alternative stylesheet" media="screen" type="text/css" title="White on Black" href="<?php $this->text('stylepath') ?>/oxygen/css.php?color=%23FFFFFF&amp;background=%23000000&amp;link=%23FF8080" />
		<link rel="alternative stylesheet" media="screen" type="text/css" title="Yellow on Blue" href="<?php $this->text('stylepath') ?>/oxygen/css.php?color=%23EEEE80&amp;background=%23000060&amp;link=%23FFAA80" />
<?php		if($this->data['pagecss'   ]) { ?>
        	<style type="text/css"><?php $this->html('pagecss'   ) ?></style>
<?php	}
        	if($this->data['usercss'   ]) { ?>
        	<style type="text/css"><?php $this->html('usercss'   ) ?></style>
		<script type="<?php $this->text('jsmimetype') ?>" src="<?php $this->text('stylepath' ) ?>/common/wikibits.js?1"><!-- wikibits js --></script>
<?php	if($this->data['jsvarurl'  ]) { ?>
		<script type="<?php $this->text('jsmimetype') ?>" src="<?php $this->text('jsvarurl'  ) ?>"><!-- site js --></script>
<?php	} ?>

<?php	}
		if($this->data['userjs'    ]) { ?>
		<script type="<?php $this->text('jsmimetype') ?>" src="<?php $this->text('userjs' ) ?>"></script>
<?php	}
		if($this->data['userjsprev']) { ?>
		<script type="<?php $this->text('jsmimetype') ?>"><?php $this->html('userjsprev') ?></script>
<?php	}
		if($this->data['trackbackhtml']) print $this->data['trackbackhtml']; ?>
		<!-- Head Scripts -->
		<?php $this->html('headscripts') ?>
	</head>
<body class="<?php $this->text('nsclass') ?> <?php $this->text('dir') ?>">
	<!-- All the header navigation is placed here -->
	<div id="header">
			<div id="header_top"><div><div>
				<img alt ="" src="/skins/oxygen/top-pardus.png"/>
				<a href="/" class="title"><?php global $wgSitename; echo $wgSitename; ?></a>
				</div></div></div>
	  	<div id="header_bottom">

		<div id="menu">
		<!-- Orderd List and Navigation Goes Here 
		  <ul>
			<li><a href="./sitemap.php">Sitemap</a></li>
			<li><a href="./contact.php">Contact Us</a></li>
		  </ul>
		 -->
		 <!-- Actions that for example allow you to edit page keep seperate! -->
			<ul>
			<?php			foreach($this->data['content_actions'] as $key => $tab) { ?>
					 <li id="ca-<?php echo htmlspecialchars($key) ?>"<?php
						if($tab['class']) { ?> class="<?php echo htmlspecialchars($tab['class']) ?>"<?php }
					 ?>><a href="<?php echo htmlspecialchars($tab['href']) ?>"><span><?php
					 echo htmlspecialchars($tab['text']) ?></span></a></li>
			<?php			 } ?>
			</ul>
		</div>
	  </div>
	</div>
		<div id="body_wrapper">
      		<div id="body">
				 <!-- Wiki Content Goes Here -->
        			<div id="right">
         				 <div class="content">
        					  <div id="main">
									<a name="top" id="top"></a>
									<?php if($this->data['sitenotice']) { ?><div id="siteNotice"><?php $this->html('sitenotice') ?></div><?php } ?>
									<h1 class="firstHeading"><?php $this->data['displaytitle']!=""?$this->text('title'):$this->html('title') ?></h1>
									<div id="bodyContent">
										<!-- <h3 id="siteSub"><?php $this->msg('tagline') ?></h3> -->
										<div id="contentSub"><?php $this->html('subtitle') ?></div>  
										<?php if($this->data['undelete']) { ?><div id="contentSub2"><?php     $this->html('undelete') ?></div><?php } ?>
										<?php if($this->data['newtalk'] ) { ?><div class="usermessage"><?php $this->html('newtalk')  ?></div><?php } ?>
<!--										<?php if($this->data['showjumplinks']) { ?><div id="jump-to-nav"><?php $this->msg('jumpto') ?> <a href="#column-one"><?php $this->msg('jumptonavigation') ?></a>, <a href="#searchInput"><?php $this->msg('jumptosearch') ?></a></div><?php } ?>-->
										<!-- start content -->
										<?php $this->html('bodytext') ?>
										<?php if($this->data['catlinks']) { ?><div id="catlinks"><?php       $this->html('catlinks') ?></div><?php } ?>
										<!-- end content -->
										<div class="visualClear"></div>
									</div>
								</div>
									</div>
									</div>
	<div id='left'>
		<!-- Search Menu -->
		<div class="menu_box">
			<form action="<?php $this->text('searchaction') ?>" id="searchform"><div>
				<input id="searchInput" name="search" type="text" <?php
					if($this->haveMsg('accesskey-search')) {
						?>accesskey="<?php $this->msg('accesskey-search') ?>"<?php }
					if( isset( $this->data['search'] ) ) {
						?> value="<?php $this->text('search') ?>"<?php } ?> />
				<input type='submit' name="fulltext" class="searchButton" value="<?php $this->msg('search') ?>" />
			</div></form>
		</div>
	<!-- End of Search Menu -->
<?php
   unset($this->data['sidebar']['SEARCH']);
   unset($this->data['sidebar']['TOOLBOX']);
   unset($this->data['sidebar']['LANGUAGES']);

   foreach ($this->data['sidebar'] as $bar => $cont) {?>
	<!-- Main Menu -->
	<div class="menutitle"><div>
		<h2><?php $out = wfMsg( $bar ); if (wfEmptyMsg($bar, $out)) echo $bar; else echo $out; ?></h2>
		</div></div>
			<div class='menu_box'>
			<ul>
                <li><a href="/Welcome_To_Pardus_Developer_Base">Home</a></li>
                <li><a href="/Getting_Started">Getting Started</a></li>
                <li><a href="/Pardus_Technologies">Technologies</a></li>
                <li><a href="/Pardus_Release_Schedule">Schedule</a></li>
                <li><a href="/Pardus_Policies">Policies</a></li>
                <li><a href="/How_Can_I_Contribute">Contribute</a></li>
		</ul>
	<?php } ?>
		</div>	

	<div class="menutitle"><div><h2><?php $this->msg('personaltools') ?></h2></div></div>
		<div class="pBody">
		<div class="menu_box">
			<ul>
<?php 		
               unset($this->data['personal_urls']['anonuserpage']);
               unset($this->data['personal_urls']['anontalk']);
               foreach($this->data['personal_urls'] as $key => $item) { ?>
                
				<li id="pt-<?php echo htmlspecialchars($key) ?>"<?php
					if ($item['active']) { ?> class="active"<?php } ?>><a href="<?php
				echo htmlspecialchars($item['href']) ?>"<?php
				if(!empty($item['class'])) { ?> class="<?php
				echo htmlspecialchars($item['class']) ?>"<?php } ?>><?php
				echo htmlspecialchars($item['text']) ?></a></li>
<?php			} ?>
			</ul>
		</div>
		</div>
	</div>
		<!-- End of Personal Tools Menu -->
<?php
		if( $this->data['language_urls'] ) { ?>
	<div id="p-lang" class="portlet">
		<h5><?php $this->msg('otherlanguages') ?></h5>
		<div class="pBody">
			<ul>
<?php		foreach($this->data['language_urls'] as $langlink) { ?>
				<li class="<?php echo htmlspecialchars($langlink['class'])?>"><?php
				?><a href="<?php echo htmlspecialchars($langlink['href']) ?>"><?php echo $langlink['text'] ?></a></li>
<?php		} ?>
			</ul>
		</div>
	</div>
<?php	} ?>
		</div>
		</div>
		<!-- Presume this is the end of the BODY -->
	</div>	
</div>
		</div>
		<div class="clear"></div>
		<div id="footer"><div id="footer_text">
           <a href="http://www.pardus.org.tr">Pardus</a>® and Pardus® logo are registered trademarks of <a href="http://uekae.tubitak.gov.tr">TÜBİTAK/UEKAE</a>.
		</div></div>
	</body>
</html>
<?php
	wfRestoreWarnings();
	} // end of execute() method


	function extractSubPageTitle(String $title)
	{
		$titles = split('/', $title);
                return  $titles[count($titles)-1];
	}

} // end of class
?>
