package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"strings"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type SearchArgs struct {
	Query string `json:"query" jsonschema:"search query"`
}

type FetchArgs struct {
	URL string `json:"url" jsonschema:"URL to fetch"`
}

func webSearch(_ context.Context, _ *mcp.CallToolRequest, args SearchArgs) (*mcp.CallToolResult, any, error) {
	apiURL := fmt.Sprintf(
		"https://api.duckduckgo.com/?q=%s&format=json&no_html=1&skip_disambig=1",
		url.QueryEscape(args.Query),
	)
	resp, err := http.Get(apiURL)
	if err != nil {
		return nil, nil, fmt.Errorf("search request failed: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, nil, err
	}

	var result map[string]any
	if err := json.Unmarshal(body, &result); err != nil {
		return nil, nil, fmt.Errorf("invalid response: %w", err)
	}

	var parts []string
	if abstract, ok := result["AbstractText"].(string); ok && abstract != "" {
		parts = append(parts, "Summary: "+abstract)
		if source, ok := result["AbstractSource"].(string); ok {
			parts = append(parts, "Source: "+source)
		}
	}
	if topics, ok := result["RelatedTopics"].([]any); ok {
		for i, t := range topics {
			if i >= 5 {
				break
			}
			if m, ok := t.(map[string]any); ok {
				if text, ok := m["Text"].(string); ok && text != "" {
					parts = append(parts, "- "+text)
				}
			}
		}
	}

	text := strings.Join(parts, "\n")
	if text == "" {
		text = "No results found for: " + args.Query
	}

	return &mcp.CallToolResult{
		Content: []mcp.Content{&mcp.TextContent{Text: text}},
	}, nil, nil
}

func fetchURL(_ context.Context, _ *mcp.CallToolRequest, args FetchArgs) (*mcp.CallToolResult, any, error) {
	resp, err := http.Get(args.URL)
	if err != nil {
		return nil, nil, fmt.Errorf("fetch failed: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(io.LimitReader(resp.Body, 50*1024))
	if err != nil {
		return nil, nil, err
	}

	return &mcp.CallToolResult{
		Content: []mcp.Content{&mcp.TextContent{Text: string(body)}},
	}, nil, nil
}

func main() {
	s := mcp.NewServer(&mcp.Implementation{Name: "search-mcp", Version: "1.0.0"}, nil)

	mcp.AddTool(s, &mcp.Tool{
		Name:        "web_search",
		Description: "Search the web using DuckDuckGo (no API key required)",
	}, webSearch)

	mcp.AddTool(s, &mcp.Tool{
		Name:        "fetch_url",
		Description: "Fetch raw content from a URL (max 50KB)",
	}, fetchURL)

	handler := mcp.NewStreamableHTTPHandler(func(_ *http.Request) *mcp.Server { return s }, nil)
	http.Handle("/mcp", handler)
	log.Println("search-mcp listening on :8080/mcp")
	log.Fatal(http.ListenAndServe(":8080", nil))
}