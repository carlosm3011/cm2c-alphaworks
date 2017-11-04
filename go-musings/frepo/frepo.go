package main

import "fmt"
import "net/http"
import "io/ioutil"
import "flag"

func getFile( url string ) []byte {
	// resp, err := http.Get("https://rdap.lacnic.net/rdap/ip/200.7.84.1")
	resp, err := http.Get(url)
    if err != nil {
        // handle error
        fmt.Println("An error has ocurred!")
    }
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)    
	return body
}

func main() {
	fmt.Println("FREPO: file repository builder and manager")
	
	// parse command line args
	var profPtr = flag.String("prof", "1.2.3.4", "profile file name")
	flag.Parse()
	var profName = *profPtr
	fmt.Println("Profile name: "+profName)

	var b []byte
	b = getFile( "https://rdap.lacnic.net/rdap/ip/" + profName )
	
    fmt.Println(string(b))
}

