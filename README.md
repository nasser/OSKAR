# OSKAR

A compiler for the OSKAR programmatic animation language targeting Houdini Python Scripts.

Designed by Larry Cuba. Implemented by Ramsey Nasser for Larry Cuba, building on work started by Bryce Summers.

## Usage
Still a work in progress. Eventually cross-platform binaries will be provided, but for now building from source is unavoidable.

You will need [node](https://nodejs.org/en/) and [dotnet](https://dotnet.microsoft.com/) installed.

```
npm install
npx arz grammar.pegjs > Generated.fs
dotnet run path/to/file.osk
```

## Implementation

The compiler is written in F#. A [parser generator written in JavaScript](https://github.com/nasser/arz) generates the parser from the `grammar.pegjs` file.