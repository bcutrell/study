package pokecache

type Cache struct {
	items map[string]interface{}
}

func NewCache() *Cache {
	return &Cache{
		items: make(map[string]interface{}),
	}
}

func (c *Cache) Get(key string) (interface{}, bool) {
	item, found := c.items[key]
	return item, found
}

func (c *Cache) Add(key string, data interface{}) {
	c.items[key] = data
}
