package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/", baseHandler)
	http.HandleFunc("/request", requestHandler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func baseHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello!")

}

func requestHandler(w http.ResponseWriter, r *http.Request) {
	// Send external request
	res, err := http.Get("https://www.google.com/")
	if err != nil {
		log.Fatalf("Error while sending request: %v\n", err)
	}

	d, err := ioutil.ReadAll(res.Body)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Fprintf(w, string(d))
}
