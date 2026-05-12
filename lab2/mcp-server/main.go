package main

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type HelloArgs struct {
	Name string `json:"name" jsonschema:"the person to greet"`
}

func main() {
	s := mcp.NewServer(&mcp.Implementation{Name: "hello-mcp", Version: "1.0.0"}, nil)

	mcp.AddTool(s, &mcp.Tool{
		Name:        "hello",
		Description: "Returns a greeting for the given name",
	}, func(ctx context.Context, _ *mcp.CallToolRequest, args HelloArgs) (*mcp.CallToolResult, any, error) {
		name := args.Name
		if name == "" {
			name = "world"
		}
		return &mcp.CallToolResult{
			Content: []mcp.Content{
				&mcp.TextContent{Text: fmt.Sprintf("Hello, %s!", name)},
			},
		}, nil, nil
	})

	handler := mcp.NewStreamableHTTPHandler(func(_ *http.Request) *mcp.Server {
		return s
	}, nil)

	http.Handle("/mcp", handler)
	log.Println("hello-mcp listening on :8080/mcp")
	log.Fatal(http.ListenAndServe(":8080", nil))
}