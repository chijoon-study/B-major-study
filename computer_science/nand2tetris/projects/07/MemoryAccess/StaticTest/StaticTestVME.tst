// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/07/MemoryAccess/StaticTest/StaticTestVME.tst

// Tests / illustrates StaticTest.vm on the VM simulator.

load StaticTest.vm,
output-file StaticTest.out,
compare-to StaticTest.cmp,

set sp 256,    // initializes the stack pointer

repeat 11 {    // StaticTest.vm has 11 instructions
  vmstep;
}

// Outputs the value at the stack's base 
output-list RAM[256]%D1.6.1;
output;
