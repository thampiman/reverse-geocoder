#ifndef REVERSE_GEOCODE_HPP 
#define REVERSE_GEOCODE_HPP
#include "Python.h"
#include <map>
#include <vector>
#include <iostream>

class ReverseGeocode
{
private:
  PyObject *pFunc;
public:
  ReverseGeocode();
  std::vector<std::map<std::string, std::string>> search(double _lat, double _lon);
};
#endif
