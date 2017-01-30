package main

import "fmt"
import "net/http"
import "io/ioutil"

func main() {
    fmt.Println("GO RDAP!")
    
    resp, err := http.Get("https://rdap.lacnic.net/rdap/ip/200.7.84.1")
    if err != nil {
        // handle error
        fmt.Println("An error has ocurred!")
    }
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)    
    fmt.Println(string(body))
}

