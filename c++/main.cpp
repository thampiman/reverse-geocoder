#include "ReverseGeocode.hpp"

#include <iostream>
int main(int argc, char **argv)
{
  if(argc < 3)
  {
    std::cerr << "please run " << argv[0] << " lat lon" << std::endl;
    exit(-1);
  }
  
  ReverseGeocode rg;
  std::vector<std::map<std::string, std::string>> results = rg.search(atof(argv[1]), atof(argv[2]));
  for (auto& result: results) {
    for (auto& x: result) {
              std::cout << x.first << " => " << x.second << '\n';
      }  
  }
}
