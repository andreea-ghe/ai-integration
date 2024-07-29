#!/bin/bash
nohup ollama serve > ollama.log 2>&1 &
sleep 10
ollama pull llama3
