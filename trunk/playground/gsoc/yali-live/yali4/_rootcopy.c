#include <Python.h>
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>



int dir_size(char *src, long *size) 
{
   
    DIR *dir;
    struct dirent *entry;
    struct stat sb;
    int fd;
    char src_file[256];


    if (!(dir = opendir(src))) 
        return 1;
    

    while ((entry = readdir(dir))) 
    {

        if (!strcmp(entry->d_name, ".") || !strcmp(entry->d_name, ".."))
           continue;

        sprintf(src_file, "%s/%s", src, entry->d_name);


        lstat(src_file, &sb);

        if (S_ISDIR(sb.st_mode)) 
        {
            if (!dir_size(src_file, size)) 
            {
                closedir(dir);
                return 1;
            }
              

        } 
    
        /*
            Sum file size 
        */

        *size += sb.st_size;
     

    }

    closedir(dir);

    return 1;
}



int copyDirectory(char *src, char *dest, PyObject *bytes) 
{
   
    DIR *dir;
    struct dirent *entry;
    struct stat sb;
    int fd, outfd;
    char buf[4096];
    char src_file[256];
    char dest_file[256];
    char link[1024];
    int i;

    PyObject *total_size, *wbytes, *seq;


    mkdir(dest, 0755);

    if (!(dir = opendir(src))) 
    {
        perror("");
        return 1;
    }

    errno = 0;
    while ((entry = readdir(dir))) 
    {





        if (!strcmp(entry->d_name, ".") || !strcmp(entry->d_name, ".."))
           continue;

        sprintf(src_file, "%s/%s", src, entry->d_name);
        sprintf(dest_file, "%s/%s", dest, entry->d_name);

        lstat(src_file, &sb);



        if (S_ISDIR(sb.st_mode)) 
        {
            if (copyDirectory(src_file, dest_file, bytes)) 
            {
                closedir(dir);
                return 1;
            }

        } 
        else if (S_ISLNK(sb.st_mode)) 
        {
            i = readlink(src_file, link, sizeof(link) - 1);
            link[i] = '\0';
            if (symlink(link, dest_file)) 
            {
                        fprintf(stderr, "Symlinking failed: %s", dest_file);
                        fflush(stderr);
            }

        }
        else 
        {

    


            fd = open(src_file, O_RDONLY);
            if (fd == -1) 
            {                   
                        fprintf(stderr, "Opening file : %s failed\n", src_file);
                        fflush(stderr);       

                closedir(dir);
                return 1;
                
            } 
	
            outfd = open(dest_file, O_RDWR | O_TRUNC | O_CREAT, 0644);
            if (outfd == -1) 
            {
                        fprintf(stderr, "Failed to create %s\n", dest_file);
                        fflush(stderr);
             
            } 
            else 
            {
                fchmod(outfd, sb.st_mode & 07777);
                
                

                while ((i = read(fd, buf, sizeof(buf))) > 0)
                {
        
                    i = write(outfd, buf, i);

                
                }
       



                close(outfd);
            }

            close(fd);
        }

        errno = 0;


    seq = PySequence_Fast(bytes, "Expects a tuple with 2 long integers");
    wbytes = PySequence_Fast_GET_ITEM(seq, 1);
    PyList_SetItem(bytes,1, PyLong_FromLong( PyLong_AsLong(wbytes) + (long)sb.st_size ));
    Py_DECREF(seq);

    }

    closedir(dir);

    return 0;
}




static PyObject *copy(PyObject *self, PyObject *args)
{

	PyObject *bytes, *src, *dest, *wbytes, *seq;

	/*
        Parse src_path, dest_path and a list for storing written bytes.
    */
	if (!PyArg_ParseTuple(args, "ssO", &src, &dest, &bytes))
	return NULL;

	

    long total_size = 0;

    dir_size(src,&total_size);


    
    seq = PySequence_Fast(bytes, "Expects a tuple with 2 long integers");
    PyList_SetItem(bytes,0, PyLong_FromLong(total_size));
    Py_DECREF(seq);

    copyDirectory(src,dest, bytes);



	return Py_BuildValue("i",1);
}


PyMethodDef methods[] = {
	{"copy", copy, METH_VARARGS, "Copies files recursively"},
	{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
init_rootcopy()
{
	(void) Py_InitModule("_rootcopy", methods);
}


