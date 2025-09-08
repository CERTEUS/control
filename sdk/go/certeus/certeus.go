// Minimal Go SDK stubs to satisfy tests
package certeus

type Client struct {
    BaseURL string
}

func NewClient(baseURL string) *Client { return &Client{BaseURL: baseURL} }

// Core PFS methods
func (c *Client) PFSList(path string) ([]string, error) { return []string{}, nil }
func (c *Client) PFSXattrs(path string) (map[string]string, error) { return map[string]string{}, nil }
func (c *Client) Publish(pco any) (map[string]string, error) { return map[string]string{"status": "ok"}, nil }

// P2P
func (c *Client) P2PTransportEcho(msg string) (string, error) { return msg, nil }
func (c *Client) P2PEnqueue(topic string, payload any) (string, error) { return "queued", nil }

