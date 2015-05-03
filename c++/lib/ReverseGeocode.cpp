#include "ReverseGeocode.hpp" 
#include <iostream>
#include <exception>

ReverseGeocode::ReverseGeocode()
{
  pFunc = NULL;
  PyObject *pName, *pModule;
  Py_Initialize();
  pName = PyString_FromString("reverse_geocoder");
  /* Error checking of pName left out */
  pModule = PyImport_Import(pName);
  Py_DECREF(pName);
  if (pModule != NULL) {
    pFunc = PyObject_GetAttrString(pModule, "search");
  }
  else
  {
    throw std::runtime_error("module not found");
  }
}

std::vector<std::map<std::string, std::string>> ReverseGeocode::search(double _lat, double _lon)
{
  std::vector<std::map<std::string, std::string>> results;
  if(pFunc && PyCallable_Check(pFunc))
  {
    PyObject *pArgs, *pLat, *pLon, *pList, *pArgs1;
    pArgs = PyTuple_New(2);
    pLat = PyFloat_FromDouble(_lat);
    if(!pLat)
    {
      std::cerr << "conversion failed" << std::endl;
      return results;
    }
    
    PyTuple_SetItem(pArgs, 0, pLat);
//     Py_DECREF(pLat);
    pLon = PyFloat_FromDouble(_lon);
    if(!pLon)
    {
      std::cerr << "conversion failed" << std::endl;
      return results;
    }
    PyTuple_SetItem(pArgs, 1, pLon);
//     Py_DECREF(pLon);

    pArgs1 = PyTuple_New(1);
    PyTuple_SetItem(pArgs1, 0, pArgs);
    pList = PyObject_CallObject(pFunc, pArgs1);
    if(!pList)
    {
      std::cout << "invalid args" << std::endl;
      PyErr_Print();
      return results;
    }
    Py_DECREF(pArgs);
    Py_DECREF(pLat);
    Py_DECREF(pLon);
    Py_DECREF(pArgs1);
    Py_ssize_t size;
    size = PyList_Size(pList);
    for(int i = 0 ; i< size; i++)
    {
      std::map<std::string, std::string> result;
      PyObject *pDict;
      pDict = PyList_GetItem(pList, i);
      PyObject *key, *value;
      Py_ssize_t pos = 0;

      while (PyDict_Next(pDict, &pos, &key, &value)) {
          const char* s = PyString_AsString(key);
          const char* s1 = PyString_AsString(value);
          result[s] = s1;
      }
      results.push_back(result);
      Py_DECREF(pDict);
      
    }
    Py_DECREF(pList);
  }
  else
  {
    std::cerr << "function not found" << std::endl;
  }
  return results;
}