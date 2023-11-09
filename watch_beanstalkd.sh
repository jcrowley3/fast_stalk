#!/bin/bash
while true; do
    clear
    echo "Fetching Beanstalkd stats..."
    echo "stats" | nc -c localhost 11300 | grep -E "(current-jobs-ready|current-jobs-reserved|total-jobs)"
    sleep 1
done
