package main

import (
	"sync"
	"time"
)

type Cache struct {
	data       map[string]cacheItem
	interval   time.Duration
	mu         sync.Mutex
	reapTicker *time.Ticker
}

type cacheItem struct {
	value      []byte
	expiration time.Time
}

func NewCache(interval time.Duration) *Cache {
	cache := &Cache{
		data:     make(map[string]cacheItem),
		interval: interval,
	}

	// Start reaping expired items
	cache.reapTicker = time.NewTicker(interval)
	go cache.reapLoop()

	return cache
}

func (c *Cache) Add(key string, value []byte) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.data[key] = cacheItem{
		value:      value,
		expiration: time.Now().Add(c.interval),
	}
}

func (c *Cache) Get(key string) ([]byte, bool) {
	c.mu.Lock()
	defer c.mu.Unlock()
	item, exists := c.data[key]
	if !exists || time.Now().After(item.expiration) {
		return nil, false
	}
	return item.value, true
}

func (c *Cache) reapLoop() {
	for {
		select {
		case <-c.reapTicker.C:
			c.reap()
		}
	}
}

func (c *Cache) reap() {
	c.mu.Lock()
	defer c.mu.Unlock()
	now := time.Now()
	for key, item := range c.data {
		if now.After(item.expiration) {
			delete(c.data, key)
		}
	}
}
