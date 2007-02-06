<?php
/*
*	This script is an extensions of original libMail by Leo West
*
*	Note by Setec Astronomy
*
*	I decided to modify and republish this script because I think it's a
*	great code! I have made some improvements like ReturnPath, a best
*	management of To, CC, BCC, Attachment and AntiSpamming headers.
*
*	Original script by Leo West - west_leo@yahoo.com
*	Original URL: http://lwest.free.fr/doc/php/lib/Mail/
*	Original Lastmod : Nov 2001
*	Original Version : 1.3
*
*	Modified by Setec Astronomy - setec@freemail.it
*	Modified URL : http://digilander.iol.it/setecastronomy/
*	Modified Lastmod : Sep 2004
*	Modified Version : 1.4.1
*
*	Credits
*	Thanks to:
*   Andrea - andreamarchetto [at] hotmail [dot] com for
* 	a small bugfix on line 342 (fopen rb windows/apache compatibility)
*   Gian Leonardo Solazzi - iw2nke [at] yahoo [dot] it for
*   a bugfix in To method.
*
*	This script is distributed  under the GPL License
*
*	This program is distributed in the hope that it will be useful,
*	but WITHOUT ANY WARRANTY; without even the implied warranty of
*	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* 	GNU General Public License for more details.
*
*	http://www.gnu.org/licenses/gpl.txt
*
*/

class Mail
{
	var $sendtoex = array();
	var $sendto = array();
	var $acc = array();
	var $abcc = array();
	var $aattach = array();
	var $fattach = array();
	var $xheaders = array();
	var $priorities = array( '1 (Highest)', '2 (High)', '3 (Normal)', '4 (Low)', '5 (Lowest)' );
	var $charset = "utf-8";
	var $ctencoding = "8bit";
	var $boundary;
	var $receipt = 0;

	function Mail () { 
		$this->boundary= "--" . md5 (uniqid ("myboundary")); 
	}

	function Subject ($subject = "") { 
		$this->xheaders['Subject'] = strtr ($subject, "\r\n" , "  "); 
		return true;
	}

	function From ($from_email, $from_name = "") {
		if (!is_string ($from_email)) { 
			return false; 
		}
		
		if (empty ($from_name)) { 
			$this->xheaders['From'] = $from_email; 
		} else { 
			$this->xheaders['From'] = "\"$from_name\" <$from_email>"; 
		}
		
		return true;
	}

	function ReplyTo ($replyto_email, $replyto_name = "") {
		if (!is_string ($replyto_email)) { 
			return false; 
		}
		
		if (empty ($replyto_email)) { 
			$this->xheaders['Reply-To'] = $replyto_email; 
		} else { 
			$this->xheaders['Reply-To'] = "\"$replyto_name\" <$replyto_email>"; 
		}

		return true;
	}

	function ReturnPath ($returnpath_email, $returnpath_name = "") { 
		if (!is_string ($returnpath_email)) { 
			return false; 
		}
		
		if (empty ($returnpath_email)) { 
			$this->xheaders['Return-Path'] = $returnpath_email; 
		} else { 
			$this->xheaders['Return-Path'] = "\"$returnpath_name\" <$returnpath_email>"; 
		}

		return true;
	}
 
	function Receipt () { 
		$this->receipt = 1; 
		return true;
	}
	
	function To ($address) {
		if (is_array ($address)) { 
			$this->sendto = array ();
			$this->sendtoex = array ();
			foreach ($address as $key => $value) {
				if (is_numeric ($key)) { 
					$this->sendto[] = $value; 
					$this->sendtoex[] = $value; 
				} elseif (is_string ($key) && is_string ($value)) { 
					$value = trim (str_replace('"', '', $value));
					$this->sendto[] = $key; 
					$this->sendtoex[] = "\"$value\" <$key>"; 
				}
			}
		} else { 
			$this->sendto[] = $address; 
			$this->sendtoex[] = $address; 
		}
		return true;
	}

	function Cc ($address) {
		if (is_array ($address)) { 
			$this->acc = array ();
			foreach ($address as $key => $value) {
				if (is_numeric ($key)) { 
					$this->acc[] = $value; 
				} elseif (is_string ($key) && is_string ($value)) { 
					$value = str_replace('"', '', $value);
					$this->acc[] = "\"$value\" <$key>"; 
				}
			}
		} else  { 
			$this->acc = array ($address); 
		}
		return true;
	}

	function Bcc ($address) {
		if (is_array ($address)) { 
			$this->abcc = array ();
			foreach ($address as $key => $value) {
				if (is_numeric ($key)) { 
					$this->abcc[] = $value; 
				} elseif (is_string ($key) && is_string ($value)) { 
					$value = str_replace('"', '', $value);
					$this->abcc[] = "\"$value\" <$key>"; 
				}
			}
		} else { 
			$this->abcc = array ($address); 
		}
		return true;
	}

	function Body ($body = "", $charset = "") {	
		$this->body = $body;
		if (!empty ($charset)) {
			$this->charset = strtolower ($charset);
			if ($this->charset != "us-ascii") { 
				$this->ctencoding = "8bit"; 
			}
		}
		return true;
	}

	function Organization ($org = "") {
		if (!empty ($org)) { 
			$this->xheaders['Organization'] = $org; 
		}
		return true;
	}

	function AntiSpaming ($client_ip = "", $proxy_server = "", $user_agent = "") {
		if (empty ($client_ip)) { 
			if (isset ($_SERVER['HTTP_X_FORWARDED_FOR']))
			{ $client_ip = $_SERVER['HTTP_X_FORWARDED_FOR']; }
			elseif (isset ($_SERVER['HTTP_CLIENT_IP']))
			{ $client_ip = $_SERVER['HTTP_CLIENT_IP']; }
			elseif (isset ($_SERVER['HTTP_FROM ']))
			{ $client_ip = $_SERVER['HTTP_FROM']; }
			elseif (isset ($_SERVER['REMOTE_ADDR']))
			{ $client_ip = $_SERVER['REMOTE_ADDR']; }
			$this->xheaders['X-HTTP-Posting-Host'] = $client_ip; 
		} else { 
			$this->xheaders['X-HTTP-Posting-Host'] = $client_ip; 
		}

		if (empty ($proxy_server)) { 
			if ($client_ip != $_SERVER['REMOTE_ADDR'])
			{ $this->xheaders['X-HTTP-Proxy-Server'] = $_SERVER['REMOTE_ADDR']; } 
		} else { 
			$this->xheaders['X-HTTP-Proxy-Server'] = $proxy_server; 
		}

		if (empty ($user_agent)) { 
			if (isset ($_SERVER['HTTP_USER_AGENT'])) { 
				$this->xheaders['X-HTTP-Posting-UserAgent'] = $_SERVER['HTTP_USER_AGENT']; 
			} else { 
				$this->xheaders['X-HTTP-Posting-UserAgent'] = "Unknown"; 
			}
		} else { 
			$this->xheaders['X-HTTP-Posting-UserAgent'] = $user_agent; 
		}

		return true;
	}
	
	function Priority ($priority = 3) {
		if (!isset ($this->priorities[$priority-1])) { 
			return false; 
		}

		$this->xheaders["X-Priority"] = $this->priorities[$priority-1]; 
		return true; 
	}
	
	function Attach ($filepath, $mimetype = "", $disposition = "inline", $filename = "") {
		if (empty ($filepath)) { 
			return false; 
		}
		
		if (empty ($mimetype)) { 
			$mimetype = "application/x-unknown-content-type"; 
		}
		
		if (empty ($filename)) { 
			$filename = basename ($filepath); 
		}
		
		$this->fattach[] = $filename;
		$this->aattach[] = $filepath;
		$this->actype[] = $mimetype;
		$this->adispo[] = $disposition;

		return true;
	}

	function BuildMail () {
		$this->headers = "";
		
		if (count ($this->sendtoex) > 0) { 
			$this->xheaders['To'] = implode (", ", $this->sendtoex); 
		}

		if (count ($this->acc) > 0) { 
			$this->xheaders['CC'] = implode (", ", $this->acc); 
		}
		
		if (count ($this->abcc) > 0) { 
			$this->xheaders['BCC'] = implode ( ", ", $this->abcc); 
		}
		
	
		if ($this->receipt) {
			if (isset ($this->xheaders["Reply-To"])) { 
				$this->xheaders["Disposition-Notification-To"] = $this->xheaders["Reply-To"]; 
			} else { 
				$this->xheaders["Disposition-Notification-To"] = $this->xheaders['From']; 
			}
		}
		
		if ($this->charset != "") {
			$this->xheaders["Mime-Version"] = "1.0";
			$this->xheaders["Content-Type"] = "text/plain; charset=$this->charset";
			$this->xheaders["Content-Transfer-Encoding"] = $this->ctencoding;
		}
	
		$this->xheaders["X-Mailer"] = "Arto Mailer/libMailv2.1";
		
		if (count ($this->aattach ) > 0) { 
			$this->_build_attachement (); 
		} else { 
			$this->fullBody = $this->body; 
		}
	
		reset ($this->xheaders);
		while (list ($hdr, $value) = each ($this->xheaders)) {
			if ($hdr != "Subject") { 
				$this->headers .= "$hdr: $value\n"; 
			}
		}
		
		return true;
	}

	function Send () {
		$this->BuildMail ();
		$strTo = implode (", ", $this->sendto);
		return mail($strTo, $this->xheaders['Subject'], $this->fullBody, $this->headers);
	}
	
	function Get () {
		$this->BuildMail ();
		$mail = $this->headers . "\n";
		$mail .= $this->fullBody;
		return $mail;
	}
	
	function _build_attachement () {
		$this->xheaders["Content-Type"] = "multipart/mixed;\n boundary=\"$this->boundary\"";

		$this->fullBody = "This is a multi-part message in MIME format.\n--$this->boundary\n";
		$this->fullBody .= "Content-Type: text/plain; charset=$this->charset\nContent-Transfer-Encoding: $this->ctencoding\n\n" . $this->body ."\n";
		
		$sep = chr(13) . chr(10);
		
		$ata = array();
		$k = 0;
		
		for ($i = 0; $i < count( $this->aattach); $i++) {
			$filename = $this->aattach[$i];
			$basename = basename($this->fattach[$i]);
			$ctype = $this->actype[$i];	// content-type
			$disposition = $this->adispo[$i];
			
			if (!file_exists ($filename)) { 
				return false; 
			}
			
			$subhdr = "--$this->boundary\nContent-type: $ctype;\n name=\"$basename\"\nContent-Transfer-Encoding: base64\nContent-Disposition: $disposition;\n  filename=\"$basename\"\n";
			$ata[$k++] = $subhdr;

			$linesz = filesize ($filename) + 1;
			$fp = fopen ($filename, 'rb');
			$ata[$k++] = chunk_split (base64_encode (fread ($fp, $linesz)));
			fclose ($fp);
		}
		$this->fullBody .= implode ($sep, $ata);
	}
} // class Mail
?>