### Initialize TS project
1. `npm init -y`
2. `npm install --save-dev typescript`
3. `npx tsc --init`
4. `mkdir src`
5. `mkdir dist`
6. Modify tsconfig.json - rootDir, outDir, target, module, moduleResolution
7. Add a linter - `npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin`
8. Add a formatter - `npm install --save-dev prettier eslint-config-prettier eslint-plugin-prettier`
9. Add TS watcher `npm i -D tsc-watch`
10. `npm i -D ts-node-dev`
10. Add scripts to package.json