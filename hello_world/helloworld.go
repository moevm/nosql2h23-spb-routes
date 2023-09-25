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


    // push data in db


    result, err := neo4j.ExecuteQuery(ctx, driver,
        "MERGE (p:Person {name: $name}) RETURN p",  
        map[string]any{  
            "name": "Alice",
        }, neo4j.EagerResultTransformer,
        neo4j.ExecuteQueryWithDatabase("neo4j"))  
    if err != nil {
        panic(err)
    }
    
    fmt.Printf("Created %v nodes in %+v.\n",
        result.Summary.Counters().NodesCreated(),
        result.Summary.ResultAvailableAfter())

    
    // get values



    result, err = neo4j.ExecuteQuery(ctx, driver,
        "MATCH (p:Person) RETURN p.name AS name",
        nil,
        neo4j.EagerResultTransformer,
        neo4j.ExecuteQueryWithDatabase("neo4j"))
    if err != nil {
        panic(err)
    }
    
    // Loop through results and do something with them
    for _, record := range result.Records {  
        name, _ := record.Get("name")  // .Get() 2nd return is whether key is present
        fmt.Println(name)
        // or
        // fmt.Println(record.AsMap())  // get Record as a map
    }
    
    // Summary information  
    fmt.Printf("The query `%v` returned %v records in %+v.\n",
        result.Summary.Query().Text(), len(result.Records),
        result.Summary.ResultAvailableAfter())


	fmt.Println("no errors")


}