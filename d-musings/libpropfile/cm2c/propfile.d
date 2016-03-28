/** 
 * libpropfile
 * m@xt6.us, 20130412 @{somewhere over the Caribbean sea, FL360}
 */
 
 module cm2c.propfile;
 
 import std.stdio;
 import std.file;
 import std.string;
 
 class PropFile {
 	private string input_fname;
 	private string[ char[] ] properties;
 	
 	// default constructor
 	this() {
 		input_fname = "";
 		properties = null;
 	}
 	
 	// set a property's value
 	void setProperty(string wkey, string wvalue) {
		assert(wkey);
 		properties[wkey] = wvalue;
 	}
 	
 	// get a property
 	string getProperty(string wkey) {
 		if (wkey in properties) {
 			return properties[wkey];
 		} else {
 			return null;
 		}
 	}
 	
 	// delete a property
 	void delProperty(string wkey) {
 		if (wkey in properties) {
 			properties.remove(wkey);
 		} 
 	}
 	
 	// dump a property file
 	void print(int wlimit = 10) {
 		foreach(k; properties.keys) {
 			writefln("%s = %s", k, properties[k]);
 		}
                writefln("  total %u properties", count());
 	}
        
        // get prop length
        ulong count() {
              return properties.keys.length;
        }
        
        // load properties from file
        bool load(string wfilename) {
              if (!exists(wfilename)) {
                   return false;  
              }
              File f = File(wfilename, "r");
              while (!f.eof()) {
                     string l = f.readln();
                     l = chomp(l);
                     // writeln(l);
                     string[string] lp = parseLine(l);
                     if (lp["type"] == "property") {
                            setProperty(lp["key"], lp["value"]);
                     }
              }
              f.close();
              return true;
        }
        
        // parse lines
        private string[string] parseLine(string wline) {
              string[string] result = null;
              result["type"] = "blank";
              int eq = indexOf(wline, "=");
              return result;
        }
 }