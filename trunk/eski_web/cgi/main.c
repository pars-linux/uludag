/* Uludag Linux: Development Infrastructure Team
 * A little CGI parses a Uludag Document (XML) and
 * outputs an HTML page using an XSLT stylesheet.
 * 
 * INPUTS: XML Document, XSLT stylesheet
 * OUTPUTS: HTML Document
 *
 * Building:
 * $ gcc -c -o scgi.o `pkg-config --cflags glib` scgi.c
 * $ gcc -Wall -o ulu.web scgi.o `pkg-config --libs --cflags libxslt glib` uluweb.c
 * $ strip ulu.web
 *
 * Baris Metin <baris@uludag.org.tr>
 */

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

#define __USE_GNU
#include <string.h>

#include <libxslt/xslt.h>
#include <libxslt/xsltInternals.h>
#include <libxslt/transform.h>
#include <libxslt/xsltutils.h>
#include <libxml/parser.h> 
#include <libxml/globals.h> 
#include "scgi.h"

#define STYLE           "stil"
#define FILE_EXT        ".xml"

#define DEFAULT_STYLE   "default.xsl"
#define DEFAULT_PAGE    "index.xml"
#define DEFAULT_LANG    "tr"
char langs[][3] = {"en", "tr"};

extern int xmlLoadExtDtdDefaultValue;


/* test if file exists */
int testfile(char* file)
{
        struct stat buf;        
        return stat(file, &buf);
}
        

/* request error */
void request_error(char* err_str)
{
        g_print("<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/><title>UluWeb: Hata</title></head><body>%s<br><br><a href=\"/\">Ana Sayfa</a></body></html>", err_str);
        return;
}


int main(int argc, char** argv)
{
	CGIVars* cgi_vars;
	xmlDocPtr doc, res;
	xsltStylesheetPtr styles;
        char *path_info;        /* relative path */
        char *path_translated;  /* absolute path */
        char *req_page;         /* requested page */
        char *req_style;        /* requested XSLT style */

	/* init SecureCGI
	 * parameters: max_cgi_len, avarage_size, max_var_len, max_data_len, max_nb_vars
	 */
	g_assert((cgi_vars = cgi_init(42000, 420, 42, 420, 42)) != NULL);
	
	/* send Content-Type */
	cgi_sendHeader(NULL);

	xmlSubstituteEntitiesDefault(1);
	xmlLoadExtDtdDefaultValue = 1;

        if (getenv("PATH_INFO")) 
                path_info = (char*) strdup(getenv("PATH_INFO"));
        if (getenv("PATH_TRANSLATED")) 
                path_translated = (char*) strdup(getenv("PATH_TRANSLATED"));

        /* find the page and parse */
        req_page = (char*) strdup(DEFAULT_PAGE);
        if (path_info) {
                if (strstr(path_info, FILE_EXT)) { /* an .xml file ? */
                        req_page = (char*) strdup(path_translated);
                } else { 
                        req_page = (char*) strdup(path_translated);
                        req_page = realloc(req_page, strlen(req_page)+strlen(DEFAULT_PAGE)+1);
                        strcat(req_page, DEFAULT_PAGE);
                }
        }

        if (!testfile(req_page)) { /* does the page exists ? */
                doc = xmlParseFile(req_page);
        } else {
                request_error("404: Sayfa bulunamadı");
                return -1;
        }
        free(req_page);

	/* read XSLT */
	if (cgi_get(cgi_vars, STYLE)) 
                req_style = (char*) strdup(cgi_get(cgi_vars, STYLE));
        else  {
                if (path_info) {
                        char *lng = (char*)strndup(path_info, sizeof(DEFAULT_LANG));
                        int i;
                        for (i=0; i<(sizeof(langs)/sizeof(DEFAULT_LANG)); i++) {
                                static char tmp[sizeof(DEFAULT_LANG)+1];
                                memset(tmp, 0, sizeof(tmp));
                                strcat(tmp, "/");
                                strcat(tmp, langs[i]);
                                if (!strcmp(tmp,lng)) { /* found the lang */
                                       req_style = (char*)malloc(strlen(lng)+strlen(DEFAULT_STYLE)+1+1);
                                       memset(req_style, 0, sizeof(req_style));
                                       strcat(req_style, langs[i]);
                                       strcat(req_style, "/");
                                       strcat(req_style, DEFAULT_STYLE);
                                }
                        }
                        free(lng);
                }
        }
                
        if (!testfile(req_style)) {
                styles = xsltParseStylesheetFile(req_style);
                res = xsltApplyStylesheet(styles, doc, NULL);
                xsltSaveResultToFile(stdout, res, styles);
                xsltFreeStylesheet(styles);
                xmlFreeDoc(res);
        } else {
                request_error("404: Stil bulunamadı");
                return -1;
        }
        
        if (req_style) free(req_style);
        free(path_info);
        free(path_translated);

	xmlFreeDoc(doc);

        xsltCleanupGlobals();
        xmlCleanupParser();

	cgi_destroy(cgi_vars);
	return(0);
}

