#include <Python.h>

typedef struct {
  PyObject_HEAD
  int* vector;
  size_t vectorSize;
} XorHash;

static void
XorHash_dealloc(XorHash* self)
{
  free(self->vector);
}

static PyObject*
XorHash_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
  XorHash* self = (XorHash*)type->tp_alloc(type, 0);
  if (self != NULL) {
    type->tp_init((PyObject*)self, args, kwds);
  }
  return (PyObject*)self;
}

static int
XorHash_init(XorHash* self, PyObject* args, PyObject* kwds)
{
  PyObject* vector;
  if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &vector)) {
    return 0;
  }

  self->vectorSize = PyList_Size(vector);
  self->vector = calloc(sizeof(int), self->vectorSize);
  for (size_t i = 0; i < self->vectorSize; ++i) {
    PyObject* item = PyList_GetItem(vector, i);
    self->vector[i] = PyInt_AsUnsignedLongMask(item);
  }

  return 0;
}

static PyObject*
XorHash_call(XorHash* self, PyObject* args, PyObject* kwds)
{
  const char* input;
  int inputLen;
  if (!PyArg_ParseTuple(args, "s#", &input, &inputLen)) {
    return NULL;
  }

  if (inputLen * 8 > self->vectorSize) {
    PyErr_SetString(PyExc_IndexError, "input is too long for vector");
    return NULL;
  }

  int h = 0;
  int j = 0;
  for (int i = 0; i < inputLen; ++i) {
    int c = input[i];
    for (int bit = 0x01; bit < 0x100; bit <<= 1) {
      if ((bit & c) != 0) {
        h ^= self->vector[j];
      }
      ++j;
    }
  }

  return Py_BuildValue("i", h);
}

static PyTypeObject XorHashType = {
  PyObject_HEAD_INIT(NULL)
  0, // ob_size
  "xorhash.XorHash", // tp_name
  sizeof(XorHash), // tp_basicsize
  0, // tp_itemsize
  (destructor)XorHash_dealloc, // tp_dealloc
  NULL, // tp_print
  NULL, // tp_getattr
  NULL, // tp_setattr
  NULL, // tp_compare
  NULL, // tp_repr
  NULL, // tp_as_number
  NULL, // tp_as_sequence
  NULL, // tp_as_mapping
  NULL, // tp_hash
  (ternaryfunc)XorHash_call, // tp_call
  NULL, // tp_str
  NULL, // tp_getattro
  NULL, // tp_setattro
  NULL, // tp_as_buffer
  Py_TPFLAGS_DEFAULT, // tp_flags
  "XorHash", // tp_doc
  NULL, // tp_traverse
  NULL, // tp_clear
  NULL, // tp_richcompare
  0, // tp_weaklistoffset
  NULL, // tp_iter
  NULL, // tp_iternext
  NULL, // tp_methods
  NULL, // tp_members
  NULL, // tp_getset
  NULL, // tp_base
  NULL, // tp_dict
  NULL, // tp_descr_get
  NULL, // tp_descr_set
  0, // tp_dictoffset
  (initproc)XorHash_init, // tp_init
  NULL, // tp_alloc
  XorHash_new, // tp_new
};

static PyMethodDef module_methods[] = {
  {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initxorhash(void)
{
  PyObject* m;

  if (PyType_Ready(&XorHashType) < 0)
    return;

  m = Py_InitModule3("xorhash", module_methods, "");
  if (m == NULL)
    return;

  Py_INCREF(&XorHashType);
  PyModule_AddObject(m, "XorHash", (PyObject*)&XorHashType);
}
