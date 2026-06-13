[org 0x7c00]

    ; 1. تهيئة قطاع الذاكرة
    mov [BOOT_DRIVE], dl
    mov bp, 0x9000
    mov sp, bp

    ; 2. تحميل النواة (Kernel) من القرص إلى الذاكرة
    mov bx, 0x1000      ; المكان الذي سنضع فيه النواة في الذاكرة
    mov dh, 1           ; عدد القطاعات (Sectors) التي سنقرأها (قطاع واحد يكفي للنواة الصغيرة)
    
    mov dl, [BOOT_DRIVE]
    mov ah, 0x02        ; وظيفة القراءة من القرص (BIOS Read)
    mov al, dh          ; عدد القطاعات
    mov ch, 0x00        ; المسار (Cylinder)
    mov dh, 0x00        ; الرأس (Head)
    mov cl, 0x02        ; ابدأ من القطاع الثاني (لأن الأول هو البوت لودر نفسه)
    int 0x13            ; استدعاء الـ BIOS

    ; 3. القفز إلى عنوان النواة لتنفيذها
    jmp 0x1000

BOOT_DRIVE db 0

times 510-($-$$) db 0
dw 0xaa55
