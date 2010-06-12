/*
 * $Id: _psutil_osx.h 347 2009-04-24 17:02:36Z jloden $
 *
 * OS X platform-specific module methods for _psutil_osx
 */

#include <Python.h>


static PyObject* get_pid_list(PyObject* self, PyObject* args);
static PyObject* get_process_info(PyObject* self, PyObject* args);
static int pid_exists(long pid);
static PyObject* get_process_cpu_times(PyObject* self, PyObject* args);
static PyObject* get_process_create_time(PyObject* self, PyObject* args);
static PyObject* get_num_cpus(PyObject* self, PyObject* args);
static PyObject* get_memory_info(PyObject* self, PyObject* args);
static PyObject* get_total_phymem(PyObject* self, PyObject* args);
static PyObject* get_avail_phymem(PyObject* self, PyObject* args);
static PyObject* get_total_virtmem(PyObject* self, PyObject* args);
static PyObject* get_avail_virtmem(PyObject* self, PyObject* args);
static PyObject* get_system_cpu_times(PyObject* self, PyObject* args);

