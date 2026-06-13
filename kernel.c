void kernel_main() {
    // العنوان 0xb8000 هو مكان "ذاكرة الفيديو" في وضع النص
    char* video_memory = (char*) 0xb8000;
    
    // كتابة حرف 'O' (الترميز 79)
    video_memory[0] = 'O';
    // لون النص (0x07 يعني نص أبيض على خلفية سوداء)
    video_memory[1] = 0x07;
}
