package main
/*

#cgo LDFLAGS: -L${SRCDIR}/ -lSummator
#include "cpp_module/wrapper_func.h"
*/
import "C"

import (
	"fmt"
    "context"
    "github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

func main() {

    // Try to use cpp from go

	a := 5
	b := 10
	sum := C.sum_from_cplus(C.int(a), C.int(b))
  	fmt.Println("res = ", sum)

	
	
	// Try to work with database



	ctx := context.Background()
    // URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
    dbUri := "neo4j://localhost"
    dbUser := "neo4j"
    dbPassword := "Andrew_07072002"
    driver, err := neo4j.NewDriverWithContext(
        dbUri,
        neo4j.BasicAuth(dbUser, dbPassword, ""))
    defer driver.Close(ctx)

    err = driver.VerifyConnectivity(ctx)
    if err != nil {
        panic(err)
    }

	fmt.Println("no errors")


}