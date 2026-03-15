#include <iostream>
#include <chrono>
#include <thread>

int main() {
    std::cout << "Program will pause for 3 seconds now...\n" << std::flush;

    // Pause the current thread for 3 seconds
    std::this_thread::sleep_for(std::chrono::seconds(3));

    std::cout << "Pause finished. Program continues and ends.\n";

    return 0;
}
