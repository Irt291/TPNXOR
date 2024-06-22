package main

import "fmt"

func main() {
	var data, output, input string
	fmt.Scanln(&data, &output)

	var q int
	fmt.Scan(&q)

	xorKey := data[0] ^ output[0]

	for i := 0; i < q; i++ {
		fmt.Scan(&input)
		for _, char := range input {
			fmt.Printf("%c", char^rune(xorKey))
		}
		fmt.Println()
	}
}
