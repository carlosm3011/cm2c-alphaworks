// ----------------------------------------------------------------------------------
// rustyrdap
// (c) carlos@xt6.us, 20161121
// ----------------------------------------------------------------------------------

use std::io::Read;
//use std::env;
// use std::fmt::Display;
extern crate docopt;
use docopt::Docopt;
extern crate hyper;
extern crate rustc_serialize;

fn main() {
    println!("RustyRDAP Client, v 0.1");
    println!("(c) carlos@xt6.us, 20161121");
    println!(" ");
    println!("Usage: ./target/rustyrdap type search_string ");
    println!("       ./target/rustyrdap ip 192.168.0.1 ");
    println!(" ");

    // recycling code from http://siciarz.net/24-days-of-rust-docopt/
    const USAGE: &'static str = "
    Usage: rustyrdap [options] <type> <query>

    Options: 
        -v, --version   display version information and exit
        -h, --help      display usage information
    ";


    #[derive(RustcDecodable)]
    struct Args {
        arg_type: Option<String>,
        arg_query: Option<String>,
        flag_version: bool,
        flag_help: bool
    }   

    // command line args
    // let args: Args = Docopt::new(USAGE).and_then(|d| d.decode()).unwrap_or_else(|e| e.exit());

    let docopt = match Docopt::new(USAGE) {
        Ok(d) => d,
        Err(e) => e.exit(),
    };
    // println!("{:?}", docopt);
    let args: Args = match docopt.decode() {
        Ok(args) => args,
        Err(e) => e.exit(),
    };    

    if args.arg_type.unwrap() == "" {

    }

    if args.arg_query.unwrap() == "" {
        
    }

    if args.flag_version {
        println!("Version: 0.0.1");
        std::process::exit(0);
    }        

    if args.flag_help {
        println!("AYUDA!");
    }

    // make request
    let client = hyper::Client::new();
    let mut rdap_rsp = client.get("https://rdap.lacnic.net/rdap/"+args.arg_type.unwrap()+"/"+args.arg_query.unwrap()).send().unwrap();
    let mut rdap_payload = "".to_string();
    let payload_len = rdap_rsp.read_to_string(&mut rdap_payload);
    //let ref rsp_headers = rdap_payload["headers"];

    println!("1. status code {}", rdap_rsp.status);
    println!("2. payload len {:?}", payload_len);
    println!("3. rdap payload {}", rdap_payload);

}
