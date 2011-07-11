#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include <libxml/xmlmemory.h>
#include <libxml/parser.h>

#define DEBUG(x) printf(x)


typedef struct vers {
    xmlChar *versionID;
    xmlChar *name;
    xmlChar *size;
    xmlChar *path;
} vers, *versPtr;


static versPtr parseVersion(xmlDocPtr doc, xmlNodePtr cur) {
    versPtr ret = NULL;

DEBUG("parseVersion\n");
    /*
     * allocate the struct
     */
    ret = (versPtr) malloc(sizeof(vers));
    if (ret == NULL) {
        fprintf(stderr,"out of memory\n");
	return(NULL);
    }
    memset(ret, 0, sizeof(vers));

    /* We don't care what the top level element name is */
    cur = cur->xmlChildrenNode;
    while (cur != NULL) {
printf("bibiiiiiiiiiiiiiiiiiiik");
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "Version"))) {
	    ret->versionID = xmlGetProp(cur, (const xmlChar *) "id");
	    if (ret->versionID == NULL) {
		fprintf(stderr, "Project has no ID\n");
	    }
	}
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "Name")) )
	    ret->name = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "Size")) )
	    ret->size = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "Path")) )
	    ret->path = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
	cur = cur->next;
    }

    return(ret);
}

/*
 * and to print it
 */
static void printVersion(versPtr cur) {
    int i;

    if (cur == NULL) return;
   	 printf("=======  Pardus\n");
    if (cur->versionID != NULL) 
	printf("versionID: %s\n", cur->versionID);
    if (cur->name != NULL) 
	printf("name: %s\n", cur->name);
    if (cur->size != NULL) 
	printf("size: %s\n", cur->size);
   if (cur->path != NULL) 
	printf("path: %s\n", cur->path);

}

typedef struct gversion {
    int nbversions;
    versPtr versions[500]; /* using dynamic alloc is left as an exercise */
} gVersion, *gVersPtr;


static gVersPtr parseGversFile(char *filename) {
    xmlDocPtr doc;
    gVersPtr ret;
    versPtr curvers;
    xmlNodePtr cur;

#ifdef LIBXML_SAX1_ENABLED
    /*
     * build an XML tree from a the file;
     */
    doc = xmlParseFile(filename);
    if (doc == NULL) return(NULL);
#else
    /*
     * the library has been compiled without some of the old interfaces
     */
    return(NULL);
#endif /* LIBXML_SAX1_ENABLED */


    cur = xmlDocGetRootElement(doc);

   
    ret = (gVersPtr) malloc(sizeof(gVersion));
    if (ret == NULL) {
        fprintf(stderr,"out of memory\n");
	xmlFreeDoc(doc);
	return(NULL);
    }
    memset(ret, 0, sizeof(gVersion));
    cur = cur->xmlChildrenNode;
    while ( cur && xmlIsBlankNode ( cur ) ) {
	cur = cur -> next;
    }
    if ( cur == 0 ) {
	xmlFreeDoc(doc);
	free(ret);
	return ( NULL );
    }

    cur = cur->xmlChildrenNode;
    while (cur != NULL) {
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "Pardus")))  {
	    curvers = parseVersion(doc , cur);
	    if (curvers != NULL)
	        ret->versions[ret->nbversions++] = curvers;
            if (ret->nbversions >= 500) break;
	}
	cur = cur->next;
    }

    return(ret);
}

int main(int argc, char **argv) {
    int i;
    gVersPtr cur;

    /* COMPAT: Do not genrate nodes for formatting spaces */
    LIBXML_TEST_VERSION
    xmlKeepBlanksDefault(0);

    for (i = 1; i < argc ; i++) {
	cur = parseGversFile(argv[i]);
	printf("bibiiiiiiiiiiiiiiiiiiik");
	if ( cur )
	  for (i = 0; i < cur->nbversions; i++) printVersion(cur->versions[i]);
	else
	  fprintf( stderr, "Error parsing file '%s'\n", argv[i]);

    }

    /* Clean up everything else before quitting. */
    xmlCleanupParser();

    return(0);
}
