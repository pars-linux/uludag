
/* Secure CGI library v1.0 */
/* (C)oderite 2000 by Frank DENIS aka Jedi/Sector One <j@4u.net> */

#include <string.h>
#include <ctype.h>
#include "scgi.h"

#define QUERY_STRING "QUERY_STRING"
#define REQUEST_METHOD "REQUEST_METHOD"
#define REQUEST_METHOD_GET "GET"
#define REQUEST_METHOD_POST "POST"
#define REQUEST_METHOD_PUT "PUT"
#define DEFAULT_TYPE "text/html"
#define CONTENT_TYPE "Content-type: "

void cgi_sendHeader(const char *type)
{
   if (type == NULL) {
      type = DEFAULT_TYPE;
   }
   g_print(CONTENT_TYPE "%s\n\n", type);
}

static char *cgi_getQueryPost(const int fd, 
			      guint max_cgi_len, guint average_size)
{
   GIOChannel *channel;
   GIOError err; 
   guint readen;
   char *buf;
   GString *str;
   char *str_str;

   g_assert(fd >= 0);
   g_assert(max_cgi_len > 1U);
   g_assert(average_size > 1U);
   g_assert(max_cgi_len >= average_size);
   buf = g_malloc(average_size);
   str = g_string_new("");
   channel = g_io_channel_unix_new(fd);   
   for (;;) {
      while ((err = g_io_channel_read(channel, buf, average_size, &readen)) ==
	     G_IO_ERROR_AGAIN);
      if (err != G_IO_ERROR_NONE || readen == 0U || 
	  memchr(buf, 0, readen) != NULL) {
	 break;
      }
      str = g_string_append(str, buf);
   }   
   g_io_channel_close(channel);
   g_free(buf);
   str_str = str->str;
   g_string_free(str, FALSE);   
   if (str_str == NULL) {
      return NULL;
   } else if (*str_str == 0) {
      g_free(str_str);
      return NULL;
   }
   return str_str;
}

static char *cgi_getQuery(guint max_cgi_len, guint average_size)
{
   gchar *request_method;
   gchar *query_string;
   
   g_assert(max_cgi_len > 1U);
   request_method = g_getenv(REQUEST_METHOD);
   query_string = g_getenv(QUERY_STRING);
   if ((request_method == NULL && query_string != NULL) ||       
       (request_method != NULL && 
	strcmp(request_method, REQUEST_METHOD_GET) == 0)) {
      if (query_string == NULL || strlen(query_string) >= (size_t) max_cgi_len) {
	 return NULL;
      }      
      return g_strdup(query_string);
   } else if (request_method == NULL ||
	      strcmp(request_method, REQUEST_METHOD_POST) == 0) {
      return cgi_getQueryPost(0, max_cgi_len, average_size);
   } else if (strcmp(request_method, REQUEST_METHOD_PUT) == 0) {
      g_warning(REQUEST_METHOD_PUT " not implemented yet\n");
      return NULL;
   } else {
      g_warning("Unkown method : [%s]\n",
		request_method == NULL ? "<none>" : request_method);
      return NULL;
   }
}

static gboolean cgi_parse(CGIVars * const cgi_vars, const char *query_string,
			  gint max_var_len, gint max_data_len, 
			  guint max_nb_vars)
{
   GString *var = NULL;
   GString *content = NULL;
   gchar g;

   g_assert(cgi_vars != NULL);
   g_assert(cgi_vars->hash_table != NULL);
   g_assert(query_string != NULL);
   g_assert(max_var_len > 0 && max_data_len > 0 && max_nb_vars > 0U);
   while (*query_string != 0) {
      var = g_string_new("");
      for (;;) {
	 g = *query_string;
	 if (g == 0) {
	    goto failure;
	 } else if (g == '+') {
	    g = ' ';
	 } else if (g == '&') {
	    goto failure;
	 } else if (g == '=') {
	    break;
	 } else if (g == '%') {
	    gchar g0;
	 
	    g0 = *++query_string;
	    if (g0 >= '0' && g0 <= '9') {
	       g0 = (g0 - '0') << 4;
	    } else if ((g0 >= 'A' && g0 <= 'F') || (g0 >= 'a' && g0 <= 'f')) {
	       g0 = toupper(g0);
	       g0 = (g0 - 'A' + 0xa) << 4;
	    } else {
	       goto failure;
	    }
	    g = *++query_string;
	    if (g >= '0' && g <= '9') {
	       g = g0 + (g - '0');
	    } else if ((g >= 'A' && g <= 'F') || (g >= 'a' && g <= 'f')) {
	       g = toupper(g);
	       g = g0 + (g - 'A' + 0xa);
	    } else {
	       goto failure;
	    }
	 } else if (g <= ' ') {
	    goto failure;
	 }
	 if (var->len >= max_var_len) {
	    goto failure;
	 }
	 var = g_string_append_c(var, g);
	 query_string++;
      }
      g_assert(*query_string != 0);
      content = g_string_new("");
      query_string++;
      for (;;) {
	 g = *query_string;
	 if (g == 0) {
	    break;
	 } else if (g == '+') {
	    g = ' ';
	 } else if (g == '=') {
	    goto failure;
	 } else if (g == '&') {
	    query_string++;
	    break;
	 } else if (g == '%') {
	    gchar g0;
	    
	    g0 = *++query_string;
	    if (g0 >= '0' && g0 <= '9') {
	       g0 = (g0 - '0') << 4;
	    } else if ((g0 >= 'A' && g0 <= 'F') || (g0 >= 'a' && g0 <= 'f')) {
	       g0 = toupper(g0);
	       g0 = (g0 - 'A' + 0xa) << 4;
	    } else {
	       goto failure;
	    }
	    g = *++query_string;
	    if (g >= '0' && g <= '9') {
	       g = g0 + (g - '0');
	    } else if ((g >= 'A' && g <= 'F') || (g >= 'a' && g <= 'f')) {
	       g = toupper(g);
	       g = g0 + (g - 'A' + 0xa);
	    } else {
	       goto failure;
	    }	 
	 } else if (g <= ' ') {
	    goto failure;
	 }
	 if (content->len >= max_data_len) {
	    goto failure;
	 }
	 content = g_string_append_c(content, g);
	 query_string++;
      }
      if (g_hash_table_lookup(cgi_vars->hash_table, var->str) != NULL) {
	 goto failure;
      }
      g_hash_table_insert(cgi_vars->hash_table, var->str, content->str);
      g_string_free(content, FALSE);
      content = NULL;
      g_string_free(var, FALSE);
      var = NULL;
      if (max_nb_vars == 0U) {
	 return FALSE;
      }      
      max_nb_vars--;      
   }   
   return TRUE;
   
   failure :
   if (content != NULL) {
      g_string_free(content, TRUE);
   }
   if (var != NULL) {
      g_string_free(var, TRUE);
   }
   return FALSE;
}

static gboolean cgi_destroy_func(gpointer key, gpointer value, gpointer data)
{
   (void) data;
   g_assert(key != NULL);
   g_free(key);   
   g_assert(value != NULL);
   g_free(value);
   
   return TRUE;
}

void cgi_destroy(CGIVars * const cgi_vars)
{
   g_assert(cgi_vars != NULL);
   g_hash_table_foreach_remove(cgi_vars->hash_table, cgi_destroy_func, NULL);
   g_hash_table_destroy(cgi_vars->hash_table);
   g_free(cgi_vars);			       
}

CGIVars *cgi_init(guint max_cgi_len, guint average_size,
		  gint max_var_len, gint max_data_len, 
		  guint max_nb_vars)
{
   CGIVars *cgi_vars;
   char *query_string;

   if ((query_string = cgi_getQuery(max_cgi_len, average_size)) == NULL) {
      return NULL;
   }   
   cgi_vars = g_new(CGIVars, 1);
   cgi_vars->hash_table = g_hash_table_new(g_str_hash, g_str_equal);
   if (cgi_parse(cgi_vars, query_string, max_var_len, 
		 max_data_len, max_nb_vars) == FALSE) {
      g_free(query_string);
      cgi_destroy(cgi_vars);
      
      return NULL;
   }   
   g_free(query_string);
   
   return cgi_vars;
}

char *cgi_get(CGIVars * const cgi_vars, const char *key)
{
   g_assert(cgi_vars != NULL);
   g_assert(cgi_vars->hash_table != NULL);
   g_assert(key != NULL && *key != 0);
   
   return g_hash_table_lookup(cgi_vars->hash_table, key);
}
