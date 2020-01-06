package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	fmt.Println("Starting HTTP server...")
	http.HandleFunc("/", BaseHandler)
	log.Fatal(http.ListenAndServe(":8080", nil))

}

func BaseHandler(w http.ResponseWriter, r *http.Request) {

}
