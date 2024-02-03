// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/08/FunctionCalls/StaticsTest/StaticsTestVME.tst

// Tests / illustrates the statics test, by executing the set and get functions
// in the VM emulator.

load,  // loads all the VM files from the current folder.
output-file StaticsTest.out,
compare-to StaticsTest.cmp,

set sp 261,

repeat 36 {
	vmstep;
}

output-list RAM[0]%D1.6.1 RAM[261]%D1.6.1 RAM[262]%D1.6.1;
output;
