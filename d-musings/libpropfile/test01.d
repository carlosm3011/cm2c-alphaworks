/**
 *
 */
 
import std.stdio;

import cm2c.propfile;

void main(string[] args) {
	writeln("well, hello there!");
	
	writeln("** test01: class instantiation");
	PropFile a;
	writeln("OK\n");
	
	writeln("** test01: property setting and getting");
	a = new PropFile();
	a.setProperty("key1", "this is a nice property");
	a.setProperty("mipr", "this is my property");
	assert( a.getProperty("key1") == "this is a nice property");
	assert( a.getProperty("mipr") == "this is my property");
	writeln("OK\n");
	
	writeln("** test01: property deletion");
	ulong n = a.count();
	a.delProperty("key1");
	assert(a.getProperty("key1") == null);
	assert(n == a.count() + 1);
	writeln("OK\n");
	
	writeln("** test02: reading properties from file");
	a.load("test01.prop");
	writeln("OK\n");		
	
	writeln("** testF: property class dump");
	a.print();
	writeln("OK\n");	
}