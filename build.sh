# 1. تجميع البوت لودر
nasm -f bin boot.asm -o boot.bin

# 2. تجميع النواة
nasm -f elf32 loader.asm -o loader.o
clang --target=i386-pc-none-elf -ffreestanding -c kernel.c -o kernel.o
ld -m elf_i386 -o kernel.bin -T linker.ld loader.o kernel.o --oformat binary

# 3. دمج الملفات في صورة واحدة (OS.img)
cat boot.bin kernel.bin > os.img

# (اختياري) ملء بقية القرص بأصفار ليكون بحجم قرص مرن حقيقي
truncate -s 1440k os.img
