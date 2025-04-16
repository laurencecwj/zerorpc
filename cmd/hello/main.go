package main

import (
	"fmt"
	"time"

	"ai.c12/zerorpc/zerorpc"
)

func main() {
	c, err := zerorpc.NewClient("tcp://0.0.0.0:4242")
	if err != nil {
		panic(err)
	}

	defer c.Close()
	response, err := c.Invoke("hello", "John")
	if err != nil {
		panic(err)
	}
	fmt.Println(response)

	_loop := 10000
	ts := time.Now()
	for range _loop {
		_, err := c.Invoke("hello", "John")
		if err != nil {
			panic(err)
		}
	}
	_dur := time.Since(ts)
	fmt.Printf("total time elapsed for [%v]: %v", _loop, _dur)
}
