extern "C"
{
#include <libavformat/avformat.h>
}

#include <iostream>
#include <cstdlib>

int main(void)
{
    av_register_all();

    std::cout << "Compile & Link FFmpeg test application correctly\n";
    return EXIT_SUCCESS;
}
