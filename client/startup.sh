#!/bin/bash
if [ -d "node_modules" ] && [ ! "$1" = "build" ]; then
  echo "node_modules already exists, skipping install"
else
  echo "Installing node_modules"
  npm install
  npm run build
fi
if [ "$1" = "deploy" ]; then
  echo "this is a deployment so not running dev server"
  exit 0
fi
npx vite serve --host 0.0.0.0
