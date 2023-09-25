#include "difficult_func.h"

int Summator::sum(int a, int b) {
    std::cout << "some computions ... " << std::endl;
    using namespace std::chrono_literals;
    std::this_thread::sleep_for(1000ms);
    std::cout << "done !" << std::endl;
    return a + b;
}