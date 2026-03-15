#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>

// A large, CPU-intensive function to find primes up to a given limit using 
// a Sieve of Eratosthenes approach (simplified/adapted for CPU load)
void generatePrimes(long long limit) {
    std::vector<bool> is_prime(limit + 1, true);
    is_prime[0] = is_prime[1] = false;
    for (long long p = 2; p * p <= limit; ++p) {
        if (is_prime[p]) {
            for (long long i = p * p; i <= limit; i += p)
                is_prime[i] = false;
        }
    }
    // Simple calculations to make it more CPU bound
    long long prime_count = 0;
    volatile double result = 0.0; // Volatile to prevent aggressive optimization
    for (long long p = 2; p <= limit; ++p) {
        if (is_prime[p]) {
            prime_count++;
            // Additional calculations to increase CPU cycles
            result += std::log(p) * std::sqrt(p); 
        }
    }
    std::cout << "Primes found up to " << limit << ": " << prime_count << " (result: " << result << ")" << std::endl;
}

int main() {
    // Set a large limit for a significant CPU load
    const long long LIMIT = 50000000; 

    auto start = std::chrono::high_resolution_clock::now();
    
    // Call the CPU-intensive function
    generatePrimes(LIMIT);

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;

    std::cout << "Execution time: " << elapsed.count() << " seconds" << std::endl;

    // A simple loop to keep the program running until user input, 
    // ensuring the console stays open when run from an IDE
    std::cout << "Press Enter to exit..." << std::endl;
    std::getchar(); 

    return 0;
}
