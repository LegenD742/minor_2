#include <iostream>
#include <cmath>
#include <vector>
#include <chrono>
#include <omp.h> // Requires OpenMP

int main() {
    // Increase this number if your CPU is exceptionally fast
    long long iterations = 40000000000; 
    
    std::cout << "Starting CPU stress test using " << omp_get_max_threads() << " threads..." << std::endl;
    
    auto start = std::chrono::high_resolution_clock::now();

    // The magic line that parallelizes the loop across all CPU cores
    #pragma omp parallel for
    for (long long i = 0; i < iterations; ++i) {
        double x = std::sqrt(std::sin(i) + 2.0); 
        // We do a dummy operation to ensure the compiler doesn't optimize the loop away
        if (x < 0) std::cout << x; 
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> diff = end - start;

    std::cout << "Finished in " << diff.count() << " seconds." << std::endl;

    return 0;
}