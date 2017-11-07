package main

import "fmt"
import "net/http"
import "io/ioutil"
import "flag"

type Profile struct {
	basedir string
	fileUrl string
	nameTemplate string
	refresh int
}

func getFile( wp Profile ) []byte {
	// resp, err := http.Get("https://rdap.lacnic.net/rdap/ip/200.7.84.1")
	resp, err := http.Get( "https://rdap.lacnic.net/rdap/ip/" + wp.nameTemplate )
    if err != nil {
        // handle error
		fmt.Println("An error has ocurred!")
		return False 
    }
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)    
	return body
}

func parseProfile() Profile {
	return Profile{".", "200.40.0.1", "whois-200.40.0.1.json", 86400}
}

func main() {
	fmt.Println("FREPO: file repository builder and manager")
	
	// parse command line args
	var profPtr = flag.String("prof", "default_profile.json", "profile file name")
	flag.Parse()
	var profName = *profPtr
	fmt.Println("Profile name: "+profName)

	// load and parse profile
	var wProfile Profile = parseProfile();

	// update file repository

	var b []byte
	b = getFile( wProfile )
	
    fmt.Println(string(b))
}

