#include "wrapper_func.h"
#include "difficult_func.h"

int sum_from_cplus(int a, int b) {
  Summator num; //create object of class SumClass
  return num.sum(a, b); // Call Sum function using wrapper function sum_from_cplus
}