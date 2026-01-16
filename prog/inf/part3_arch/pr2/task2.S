.include "my-macro"	# подключение файла с макроопределениями

.text
        
.global _start
_start:	
	nop
        movl $5, %eax
	movl $1, %ebx

L1: 	
        cmpl  $0, %eax
	je    L2
	imull %eax, %ebx
	decl  %eax
	jmp   L1
	
L2:	
        Finish
.end
        
