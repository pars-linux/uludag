
/* Secure CGI library v1.0 */
/* (C)oderite 2000 by Frank DENIS aka Jedi/Sector One <j@4u.net> */

#include <glib.h>

#ifndef __SCGI_H__
#define __SCGI_H__ 1

typedef struct CGIVars_ {
   GHashTable *hash_table;  
} CGIVars;

CGIVars *cgi_init(guint max_cgi_len, guint average_size,
		  gint max_var_len, gint max_data_len, 
		  guint max_nb_vars);

char *cgi_get(CGIVars * const cgi_vars, const char *key);
void cgi_destroy(CGIVars * const cgi_vars);
void cgi_sendHeader(const char * const type);

#endif
