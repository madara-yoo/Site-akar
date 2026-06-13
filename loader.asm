[bits 32]
section .text
    global _start
    extern kernel_main

_start:
    call kernel_main
    hlt           ; إيقاف المعالج بعد الانتهاء
